from unsloth import FastLanguageModel
from unsloth import is_bfloat16_supported
import torch
from transformers import TrainerCallback
from trl import SFTTrainer, SFTConfig
import wandb
import argparse
import random
import shutil
import sys
import config

# Import the dynamic dataset
from dynamic_dataset import DynamicPoemDataset
from format_config import AuthorFormat

argparser = argparse.ArgumentParser(description="Unsloth Llama LoRA Dynamic Dataset Training Script")
argparser.add_argument("--cont", action="store_true", help="Continue training from the last checkpoint")
argparser.add_argument("--wandb_id", type=str, default=None, help="WandB run ID to resume from")
argparser.add_argument("--model", type=str, default="unsloth/Meta-Llama-3.1-8B", help="Base model name")
argparser.add_argument("--checkpoint", type=str, default=None, help="Checkpoint directory to resume from")
argparser.add_argument("--run_name", type=str, help="Name of the run for WandB")
argparser.add_argument("--epochs", type=float, default=10, help="Number of epochs to train for")
argparser.add_argument("--batch", type=int, default=16, help="Batch size per device during training")
argparser.add_argument("--grad_accum", type=int, default=8, help="Gradient accumulation steps")
argparser.add_argument("--max_l", type=int, default=4096, help="Maximum sequence length (tokens); longer samples are truncated")
argparser.add_argument("--lr", type=float, default=1e-4, help="Learning rate")
argparser.add_argument("--warmup_ratio", type=float, default=0.03, help="Warmup ratio")
argparser.add_argument("--weight_decay", type=float, default=0.01, help="Weight decay")
argparser.add_argument("--save_total_limit", type=int, default=3, help="Keep at most this many checkpoints")
argparser.add_argument("--save_steps", type=int, default=200, help="Save a checkpoint every N optimizer steps (resume with --cont)")
argparser.add_argument("--eval_batch", type=int, default=2, help="Eval batch size per device (eval needs full-vocab logits, keep small)")
argparser.add_argument("--eval_max_poems", type=int, default=300, help="Cap on the number of held-out eval poems (0 = no cap)")
argparser.add_argument("--no_group_by_length", action="store_true", help="Disable length-grouped batching (it cuts padding waste but costs a few minutes of tokenisation at start)")
argparser.add_argument("--seed", type=int, default=42, help="Seed for the trainer and for the random format choices")
argparser.add_argument("--db_path", type=str, default=config.DB_PATH, help="Path to SQLite database")
argparser.add_argument("--max_poems", type=int, default=None, help="Maximum number of poems to load (None = all)")
argparser.add_argument("--eval_frac", type=float, default=0, help="Fraction of books held out for eval, e.g. 0.01 (default 0 = train on everything, no eval)")
argparser.add_argument("--oversample", type=str, action="append", default=[],
                       help='Repeat an author\'s poems N times per epoch, e.g. --oversample "Hrabě, Václav:20" (repeatable)')
argparser.add_argument("--author_full_prob", type=float, default=None,
                       help="Probability that a sample carries the full author name (default: uniform over the 4 author formats, i.e. 0.25)")
argparser.add_argument("--no_append_eos", action="store_true", help="Do not append the EOS token to training samples")
argparser.add_argument("--debug", action="store_true", help="Debug mode: 10 poems, 5 epochs, log all generated training data")
args = argparser.parse_args()

if args.debug:
    args.max_poems = 10
    args.epochs = 5
    args.eval_frac = 0

random.seed(args.seed)

oversample = {}
for spec in args.oversample:
    author, _, n = spec.rpartition(':')
    oversample[author] = int(n)

author_weights = None
if args.author_full_prob is not None:
    rest = (1 - args.author_full_prob) / 3
    author_weights = {AuthorFormat.FULL: args.author_full_prob, AuthorFormat.NAME_SURNAME: rest,
                      AuthorFormat.OMIT: rest, AuthorFormat.PREDICT: rest}

# Load the model first: we need the tokenizer's EOS token for the dataset
max_seq_length = args.max_l
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = args.checkpoint if args.checkpoint else args.model,
    max_seq_length = max_seq_length,
    dtype = torch.bfloat16,
    load_in_4bit = False,
)

# Create dynamic dataset
# DynamicPoemDataset has a map() method for SFTTrainer compatibility while
# keeping dynamic format generation in __getitem__ (a new format variant per access).
print("Loading dynamic dataset from database...")
debug_log = config.LOG_PATH + "debug_training_data.txt" if args.debug else None
full_dataset = DynamicPoemDataset(db_path=args.db_path, max_poems=args.max_poems, log_path=debug_log,
                                  random_seed=args.seed, author_weights=author_weights,
                                  append_eos=None if args.no_append_eos else tokenizer.eos_token)
print(f"Dataset loaded: {len(full_dataset)} poems, {len(full_dataset.dropped)} dropped.")
if full_dataset.dropped:
    dropped_path = config.LOG_PATH + f"dropped_poems_{args.run_name}.txt"
    with open(dropped_path, "w") as f:
        for pid, err in full_dataset.dropped:
            print(pid, err, file=f)
    print(f"Dropped poem ids written to {dropped_path}")

my_dataset, eval_dataset = full_dataset.split_by_books(args.eval_frac, seed=args.seed)
if eval_dataset is not None and args.eval_max_poems and len(eval_dataset) > args.eval_max_poems:
    eval_dataset = eval_dataset._clone_with_poems(eval_dataset.poems[:args.eval_max_poems])
if oversample:
    my_dataset = my_dataset.oversample(oversample, seed=args.seed)
print(f"Train poems: {len(my_dataset)}; eval poems: {len(eval_dataset) if eval_dataset else 0}")
print("Dynamic formatting will be applied during training.")

run_name = args.run_name

params = {"name": run_name}
if args.cont:
    params["resume"] = 'must'
    params["id"] = args.wandb_id
wandb.init(
    entity='tomasmcz-charles-university',
    project='edupo',
    **params
    )

if not args.cont and args.checkpoint is None:
    # Do model patching and add fast LoRA weights
    model = FastLanguageModel.get_peft_model(
        model,
        r = 64,
        target_modules = ["q_proj", "k_proj", "v_proj", "o_proj",
                      "gate_proj", "up_proj", "down_proj",],
        lora_alpha = 64,
        lora_dropout = 0, # Supports any, but = 0 is optimized
        bias = "none",    # Supports any, but = "none" is optimized
        # [NEW] "unsloth" uses 30% less VRAM, fits 2x larger batch sizes!
        use_gradient_checkpointing = "unsloth", # True or "unsloth" for very long context
        random_state = 3407,
        max_seq_length = max_seq_length,
    )

# NOTE: with trl >= 0.20 the sequence length, packing and text field must be
# given in SFTConfig; passing them as SFTTrainer kwargs is silently ignored
# (the previous version of this script trained with max_length=1024 that way).
# Packing is disabled explicitly: Unsloth's patched trainer disables it anyway.
sft_config = SFTConfig(
    per_device_train_batch_size = args.batch,
    gradient_accumulation_steps = args.grad_accum,
    num_train_epochs = args.epochs,
    learning_rate = args.lr,
    warmup_ratio = args.warmup_ratio,
    weight_decay = args.weight_decay,
    lr_scheduler_type = "linear",
    fp16 = not is_bfloat16_supported(),
    bf16 = is_bfloat16_supported(),
    logging_steps = 1,
    optim = "adamw_8bit",
    seed = args.seed,
    output_dir = config.OUTPUT_PREFIX + run_name,
    run_name = run_name,
    save_strategy = "steps",
    save_steps = args.save_steps,
    save_total_limit = args.save_total_limit,
    eval_strategy = "epoch" if eval_dataset else "no",
    per_device_eval_batch_size = args.eval_batch,
    eval_accumulation_steps = 4,
    # Unsloth's SFTConfig defaults this to True: on an OOM (e.g. in eval) accelerate then
    # shrinks the batch and silently RESTARTS the whole training loop from step 0.
    auto_find_batch_size = False,
    # Batches of similar-length poems -> little padding. Without packing this is what
    # keeps 4096-token max_length from making every step 5x slower. The sampler
    # tokenises every sample once at train start to learn the lengths (a few minutes).
    group_by_length = not args.no_group_by_length,
    max_length = max_seq_length,
    packing = False,
    dataset_text_field = "text",
    report_to = "wandb",
)

trainer = SFTTrainer(
    model = model,
    args = sft_config,
    train_dataset = my_dataset,
    eval_dataset = eval_dataset,
    processing_class = tokenizer,
)

# Sanity checks on what the trainer will actually feed the model
print(f"Effective trainer args: max_length={trainer.args.max_length} packing={trainer.args.packing} "
      f"lr={trainer.args.learning_rate} epochs={trainer.args.num_train_epochs} eval={trainer.args.eval_strategy} "
      f"eval_batch={trainer.args.per_device_eval_batch_size} save_steps={trainer.args.save_steps} "
      f"group_by_length={trainer.args.group_by_length} auto_find_batch_size={trainer.args.auto_find_batch_size}")
assert not trainer.args.auto_find_batch_size, "auto_find_batch_size must stay off (it restarts training from scratch on OOM)"
sample = trainer.train_dataset[0]
if "input_ids" in sample:
    ids = sample["input_ids"]
else:  # dataset not pre-tokenised by the trainer; tokenise the way the collator would
    ids = tokenizer(sample["text"], add_special_tokens=True)["input_ids"]
print(f"Sample 0: {len(ids)} tokens, first={ids[:2]} last={ids[-2:]}, eos_token_id={tokenizer.eos_token_id}")
if not args.no_append_eos:
    assert ids[-1] == tokenizer.eos_token_id, \
        "Training samples do not end with EOS; the model would never learn to stop generating."
    assert ids[0] == tokenizer.bos_token_id and ids[1] != tokenizer.bos_token_id, "Unexpected BOS handling"
n_over = sum(1 for _ in range(min(len(trainer.train_dataset), 200))
             if len(trainer.train_dataset[_].get("input_ids", [])) >= max_seq_length)
print(f"Of the first 200 samples, {n_over} hit the max_length={max_seq_length} limit (truncated).")

# Rolling checkpoint-N dirs (every --save_steps, at most --save_total_limit) are managed by
# the trainer. On top of that, force a full checkpoint (adapter + optimizer + scheduler +
# RNG state, i.e. resumable with --cont) at the end of every epoch and copy it to epoch-N;
# those copies are never rotated away.
class EpochSnapshotCallback(TrainerCallback):
    def __init__(self):
        self.pending_epoch = None

    def on_epoch_end(self, args, state, control, **kwargs):
        self.pending_epoch = round(state.epoch)
        control.should_save = True
        return control

    def on_save(self, args, state, control, **kwargs):
        if self.pending_epoch is None:
            return control
        src = f"{args.output_dir}/checkpoint-{state.global_step}"
        dst = f"{args.output_dir}/epoch-{self.pending_epoch}"
        print(f"Copying end-of-epoch checkpoint {src} -> {dst}")
        shutil.copytree(src, dst, dirs_exist_ok=True)
        self.pending_epoch = None
        return control
trainer.add_callback(EpochSnapshotCallback())

if debug_log:
    class EpochLogCallback(TrainerCallback):
        def on_epoch_begin(self, args, state, control, **kwargs):
            my_dataset.log_marker(f"epoch {int(state.epoch) + 1}")
            my_dataset.log_epoch_samples()
    trainer.add_callback(EpochLogCallback())

if args.cont:
    trainer.train(resume_from_checkpoint = True)
else:
    trainer.train()

# TODO:
#   - evaluace
