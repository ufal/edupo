from unsloth import FastLanguageModel
from unsloth import is_bfloat16_supported
import torch
from transformers import TrainingArguments
from trl import SFTTrainer
from datasets import load_dataset, Dataset
import wandb
import argparse
import sys

# Import the dynamic dataset
sys.path.append("data_for_LM")
from dynamic_dataset import DynamicPoemDataset

argparser = argparse.ArgumentParser(description="Unsloth Llama LoRA Dynamic Dataset Training Script")
argparser.add_argument("--cont", action="store_true", help="Continue training from the last checkpoint")
argparser.add_argument("--wandb_id", type=str, default=None, help="WandB run ID to resume from")
argparser.add_argument("--model", type=str, default="unsloth/Meta-Llama-3.1-8B", help="Base model name")
argparser.add_argument("--checkpoint", type=str, default=None, help="Checkpoint directory to resume from")
argparser.add_argument("--run_name", type=str, help="Name of the run for WandB")
argparser.add_argument("--epochs", type=int, default=10, help="Number of epochs to train for")
argparser.add_argument("--batch", type=int, default=16, help="Batch size per device during training")
argparser.add_argument("--max_l", type=int, default=2048, help="Maximum sequence length for training")
argparser.add_argument("--db_path", type=str, default="new.db", help="Path to SQLite database")
argparser.add_argument("--max_poems", type=int, default=None, help="Maximum number of poems to load (None = all)")
args = argparser.parse_args()

# Create dynamic dataset
# DynamicPoemDataset now has a map() method for SFTTrainer compatibility
# while maintaining dynamic format generation in __getitem__
print("Loading dynamic dataset from database...")
my_dataset = DynamicPoemDataset(db_path=args.db_path, max_poems=args.max_poems)
print(f"Dataset loaded: {len(my_dataset)} poems")
print("Dynamic formatting will be applied during training.")

max_seq_length = args.max_l

run_name = args.run_name

params = {}
if args.cont:
    params["resume"] = 'must'
    params["id"] = args.wandb_id
wandb.init(
    entity='tomasmcz-charles-university',
    project='edupo',
    **params
    #id="b457ktf0",
    #name=run_name,
    #resume='must'
    )

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = args.checkpoint if args.checkpoint else args.model,
    max_seq_length = max_seq_length,
    dtype = torch.bfloat16,
    load_in_4bit = False,
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

# Dataset is shuffled by default in DynamicPoemDataset
# Dynamic formatting happens in __getitem__, so each epoch sees new format variations
trainer = SFTTrainer(
    model = model,
    args = TrainingArguments(
        per_device_train_batch_size = args.batch,
        gradient_accumulation_steps = 8,
        #warmup_ratio = 0.1,
        num_train_epochs = args.epochs,
        fp16 = not is_bfloat16_supported(),
        bf16 = is_bfloat16_supported(),
        logging_steps = 1,
        optim = "adamw_8bit",
        seed = 42,
        output_dir = "outputs/" + run_name,
        run_name = run_name,# + "_cont",
        save_strategy = "epoch",
        # TODO weight decay, scheduler, lr?
    ),
    train_dataset = my_dataset,
    # eval_dataset = YOUR_DATASET_HERE,
    tokenizer = tokenizer,
    max_seq_length = max_seq_length,
    dataset_text_field = "text",
    packing = True,
)
if args.cont:
    trainer.train(resume_from_checkpoint = True)
else:
    trainer.train()

# TODO:
#   - evaluace
