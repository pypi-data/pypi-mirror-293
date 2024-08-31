HUGGING_FACE = "huggingface"
EOS_BUCKET = "eos-bucket"
DATASET_TYPES_LIST = [HUGGING_FACE, EOS_BUCKET]

LLAMA2 = "meta-llama/Llama-2-7b-hf"
LLAMA3_8B = "meta-llama/Meta-Llama-3-8B"
LLAMA3_8B_INST = "meta-llama/Meta-Llama-3-8B-Instruct"
MISTRAL_7B = "mistralai/Mistral-7B-v0.1"
MISTRAL_7B_INST = "mistralai/Mistral-7B-Instruct-v0.2"
MISTRAL_8X7B = "mistralai/Mixtral-8x7B-v0.1"
GEMMA_7B = "google/gemma-7b"
GEMMA_7B_INST = "google/gemma-7b-it"
STABLE_DIFFUSION_2_1 = "stabilityai/stable-diffusion-2-1"
STABLE_DIFFUSION_SDXL = "stabilityai/stable-diffusion-xl-base-1.0"

TEXT_MODELS_LIST = [
   LLAMA2, LLAMA3_8B, MISTRAL_7B,
   MISTRAL_8X7B, GEMMA_7B, MISTRAL_7B_INST,
   GEMMA_7B_INST, LLAMA3_8B_INST,
   ]
IMAGE_MODELS_LIST = [
   STABLE_DIFFUSION_SDXL,
   STABLE_DIFFUSION_2_1,
   ]
COMBINED_MODELS_LIST = TEXT_MODELS_LIST + IMAGE_MODELS_LIST
CLIENT_NOT_READY_MESSAGE = "Client is not ready. Please initiate client by using: \ne2enetworks.cloud.tir.init(...)"
PIPELINE = "pipeline"
ALLOWED_DATATYPES_ERROR = "Dataset type: Only huggingface and eos-bucket allowed"
INVALID_DATASET = "Invalid dataset"
PLAN_NAME_ERROR = "plan_name is should be a string"
DEFAULT_TEXT_TRAINING_ARGS = {
    "validation_split_ratio": (float, 0.1, False),
    "target_dataset_field": (str, 'text', False),
    "gradient_accumulation_steps": (int, 1, False),
    "context_length": (int, 512, False),
    "learning_rate": (float, 0.0000141, False),
    "epochs": (int, 3, False),
    "stop_training_when": (str, "epoch_count", False),
    "max_steps": (int, -1, False),
    "batch_size": (int, 4, False),
    "peft_lora_alpha": (int, 16, False),
    "peft_lora_r": (int, 64, False),
    "save_strategy": (str, "no", False),
    "task": (str, "Instruction-Finetuning", False),
    "prompt_configuration": (str, "", False),
    "save_steps": (int, 10, False),
    "limit_training_records_count": (int, -1, False),
    "limit_eval_records_count": (int, -1, False),
    "source_repository_type": (str, "base_model", False),
    "source_model_repo_info": (str, "", False),
    "source_model_path": (str, "", False),
    "save_total_limit": (int, 10, False),
    "lora_dropout": (float, 0.05, False),
    "lora_bias": (str, "none", False),
    "load_in_4bit": (bool, False, False),
    "bnb_4bit_compute_dtype": (str, "bfloat16", False),
    "bnb_4bit_quant_type": (str, "fp4", False),
    "bnb_4bit_use_double_quant": (bool, False, False),
    "train_batch_size": (int, 1, False),
}
DEFAULT_IMAGE_TRAINING_ARGS = {
    "gradient_accumulation_steps": (int, 1, False),
    "learning_rate": (float, 0.0000141, False),
    "epochs": (int, 3, False),
    "stop_training_when": (str, "epoch_count", False),
    "max_steps": (int, -1, False),
    "batch_size": (int, 4, False),
    "peft_lora_alpha": (int, 16, False),
    "peft_lora_r": (int, 64, False),
    "save_strategy": (str, "no", False),
    "task": (str, "Instruction-Finetuning", False),
    "save_steps": (int, 10, False),
    "limit_training_records_count": (int, -1, False),
    "source_repository_type": (str, "base_model", False),
    "source_model_repo_info": (str, "", False),
    "source_model_path": (str, "", False),
    "save_total_limit": (int, 10, False),
    "image_column": (str, "image", False),
    "caption_column": (str, "text", False),
    "validation_prompt": (str, "A photo of a man with green eyes", False),
    "num_validation_images": (int, 2, False),
    "train_batch_size": (int, 1, False),
    "load_in_8bit": (bool, False, False),
    "mixed_precision": (str, "no", False),
    "checkpointing_steps": (int, 500, False),
    "checkpoints_total_limit": (int, 10, False)
}
INVALID_MODEL_NAME = f"Model name must be in {COMBINED_MODELS_LIST}"
