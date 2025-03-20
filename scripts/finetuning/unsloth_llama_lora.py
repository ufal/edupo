from unsloth import FastLanguageModel
from unsloth import is_bfloat16_supported
import torch
from transformers import TrainingArguments
from trl import SFTTrainer
from datasets import load_dataset, Dataset

my_dataset = Dataset.from_json("lm_data.json") #load_dataset("json", data_files="lm_data.json", field="text")

max_seq_length = 1024

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "unsloth/Meta-Llama-3.1-8B",
    max_seq_length = max_seq_length,
    dtype = torch.bfloat16,
    load_in_4bit = False,
)

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

run_name = "unsloth_llama_lora_002_u"

# TODO does this shuffle the dataset?
trainer = SFTTrainer(
    model = model,
    args = TrainingArguments(
        per_device_train_batch_size = 16,
        gradient_accumulation_steps = 8,
        warmup_ratio = 0.1,
        num_train_epochs = 10,
        fp16 = not is_bfloat16_supported(),
        bf16 = is_bfloat16_supported(),
        logging_steps = 1,
        optim = "adamw_8bit",
        seed = 42,
        output_dir = "outputs/" + run_name,
        run_name = run_name,
        # TODO weight decay, scheduler, lr?
    ),
    train_dataset = my_dataset,
    # eval_dataset = YOUR_DATASET_HERE,
    tokenizer = tokenizer,
    max_seq_length = max_seq_length,
    dataset_text_field = "text",
    packing = True,
)
trainer.train()

# TODO:
#   - evaluace
#   - deduplikace datasetu