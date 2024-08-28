from typing import Any, Dict, Optional, Literal, Union
import os
from lightmodelfactory.util.logger import logger
from dataclasses import dataclass,field

args_env_dict = {
    "PLUGIN_NAME":"",
    "STAGE":"",
    "FINETUNING_TYPE": "",
    "PRETRAINED_MODEL_NAME":"",
    "DATASET_DESC":"",
    "DATASET":"",
    "PER_DEVICE_TRAIN_BATCH_SIZE":"",
    "ADAPTER_NAME_OR_PATH":"",
    "MODEL_NAME_OR_PATH":"",
    "OUTPUT_DIR":"",
    "NUM_TRAIN_EPOCHS":"",
    "LEARNING_RATE":"",
    "CUTOFF_LEN":"",
    "VAL_SIZE":"",
    "LORA_ALPHA":"",
    "LORA_DROPOUT":"",
    "LORA_RANK":"",
    "LORA_TARGET":"",
    "QUANTIZATION_BIT":"",
    "USE_GALORE":"",
    "USE_BADAM":"",
    "FLASH_ATTN":"",
    "USE_UNSLOTH":"",
    "VISUAL_INPUTS":"",
    "OVERWRITE_OUTPUT_DIR":"",
    "NPROC_PER_NODE":"",
    "MERGE_LORA":"",
    "USE_FSDP":"",
    "GRADIENT_ACCUMULATION_STEPS":"",
    "WEIGHT_DECAY":"",
    "MAX_GRAD_NORM":"",
    "LR_SCHEDULER_TYPE":"",
    "WARMUP_RATIO":"",
    "WARMUP_STEPS":"",
    "OPTIM":"",
    "SAVE_STRATEGY":"",
    "SAVE_STEPS":"",
    "SAVE_TOTAL_LIMIT":"",
}

@dataclass
class PluginArguments:
    plugin_name : str = field(default="llama_factory")
    pretrained_model_name : str = field(default=None)
    dataset_desc : str = field(default=None)
    end_to_zip : bool = field(default=True,)
    nproc_per_node : int = field(default=1,)
    merge_lora :bool = field(default=False,)
    use_fsdp : bool = field(default=False,)

@dataclass
class DataArguments:
    dataset: Optional[str] = field(
        default=None,
        metadata={"help": "The name of provided dataset(s) to use. Use commas to separate multiple datasets."},
    )
    eval_dataset: Optional[str] = field(
        default=None,
        metadata={"help": "The name of dataset(s) to use for evaluation. Use commas to separate multiple datasets."},
    )
    template: Optional[str] = field(
        default=None,
        metadata={"help": "Which template to use for constructing prompts in training and inference."},
    )
    cutoff_len:int = field(
        default=1024,
        metadata={"help": "The cutoff length of the tokenized inputs in the dataset."},
    )
    val_size: float = field(
        default=0.0,
        metadata={"help": "Size of the development set, should be an integer or a float in range `[0,1)`."},
    )
    neat_packing: bool = field(
        default=False,
        metadata={"help": "Enable sequence packing without cross-attention."},
    )
    mix_strategy: Literal["concat", "interleave_under", "interleave_over"] = field(
        default="concat",
        metadata={"help": "Strategy to use in dataset mixing (concat/interleave) (undersampling/oversampling)."},
    )
    interleave_probs: Optional[str] = field(
        default=None,
        metadata={"help": "Probabilities to sample data from datasets. Use commas to separate multiple datasets."},
    )
    streaming: bool = field(
        default=False,
        metadata={"help": "Enable dataset streaming."},
    )
@dataclass
class FinetuningArguments():
    r"""
    Arguments pertaining to which techniques we are going to fine-tuning with.
    """

    pure_bf16: bool = field(
        default=False,
        metadata={"help": "Whether or not to train model in purely bf16 precision (without AMP)."},
    )
    stage: Literal["pt", "sft", "rm", "ppo", "dpo", "kto"] = field(
        default="sft",
        metadata={"help": "Which stage will be performed in training."},
    )
    finetuning_type: Literal["lora", "freeze", "full"] = field(
        default="lora",
        metadata={"help": "Which fine-tuning method to use."},
    )
    lora_alpha: Optional[int] = field(
        default=16,
        metadata={"help": "The scale factor for LoRA fine-tuning (default: lora_rank * 2)."},
    )
    lora_dropout: float = field(
        default=0.1,
        metadata={"help": "Dropout rate for the LoRA fine-tuning."},
    )
    lora_rank: int = field(
        default=8,
        metadata={"help": "The intrinsic dimension for LoRA fine-tuning."},
    )
    lora_target: str = field(
        default="all",
        metadata={
            "help": (
                "Name(s) of target modules to apply LoRA. "
                "Use commas to separate multiple modules. "
                "Use `all` to specify all the linear modules."
            )
        },
    )
    use_galore: bool = field(
        default=False,
        metadata={"help": "Whether or not to use the gradient low-Rank projection (GaLore)."},
    )
    use_badam: bool = field(
        default=False,
        metadata={"help": "Whether or not to use the BAdam optimizer."},
    )
    plot_loss: bool = field(
        default=True,
        metadata={"help": "Whether or not to save the training loss curves."},
    )
    pref_loss: Literal["sigmoid", "hinge", "ipo", "kto_pair", "orpo", "simpo"] = field(
        default="sigmoid",
        metadata={"help": "The type of DPO loss to use."},
    )

@dataclass
class ModelArguments:
    model_name_or_path: str
    adapter_name_or_path: Optional[str] = field(
        default=None,
        metadata={
            "help": (
                "Path to the adapter weight or identifier from huggingface.co/models. "
                "Use commas to separate multiple adapters."
            )
        },
    )
    quantization_bit: Optional[int] = field(
        default=None,
        metadata={"help": "The number of bits to quantize the model using bitsandbytes."},
    )
    flash_attn: Literal["off", "sdpa", "fa2", "auto"] = field(
        default="auto",
        metadata={"help": "Enable FlashAttention for faster training and inference."},
    )
    use_unsloth: bool = field(
        default=False,
        metadata={"help": "Whether or not to use unsloth's optimization for the LoRA training."},
    )
    visual_inputs: bool = field(
        default=False,
        metadata={"help": "Whethor or not to use multimodal LLM that accepts visual inputs."},
    )

@dataclass
class TrainingArguments():
    bf16: bool = field(
        default=False,
        metadata={
            "help": (
                "Whether to use bf16 (mixed) precision instead of 32-bit. Requires Ampere or higher NVIDIA"
                " architecture or using CPU (use_cpu) or Ascend NPU. This is an experimental API and it may change."
            )
        },
    )
    fp16: bool = field(
        default=True,
        metadata={"help": "Whether to use fp16 (mixed) precision instead of 32-bit"},
    )
    output_dir: str = field(
        default=None,
        metadata={"help": "The output directory where the model predictions and checkpoints will be written."},
    )
    overwrite_output_dir: bool = field(
        default=False,
        metadata={
            "help": (
                "Overwrite the content of the output directory. "
                "Use this to continue training if output_dir points to a checkpoint directory."
            )
        },
    )
    gradient_accumulation_steps: int = field(
        default=1,
        metadata={"help": "Number of updates steps to accumulate before performing a backward/update pass."},
    )
    learning_rate: float = field(default=5e-5, metadata={"help": "The initial learning rate for AdamW."})
    weight_decay: float = field(default=0.0, metadata={"help": "Weight decay for AdamW if we apply some."})
    max_grad_norm: float = field(default=1.0, metadata={"help": "Max gradient norm."})
    num_train_epochs: float = field(default=3.0, metadata={"help": "Total number of training epochs to perform."})
    lr_scheduler_type: Literal["cosine", "linear"] = field(
        default="cosine",
        metadata={"help": "The scheduler type to use."},
    )
    warmup_ratio: float = field(
        default=0.0, metadata={"help": "Linear warmup over warmup_ratio fraction of total steps."}
    )
    warmup_steps: int = field(default=0, metadata={"help": "Linear warmup over warmup_steps."})
    logging_steps: float = field(
        default=10,
        metadata={
            "help": (
                "Log every X updates steps. Should be an integer or a float in range `[0,1)`. "
                "If smaller than 1, will be interpreted as ratio of total training steps."
            )
        },
    )
    save_strategy: Literal["no", "epoch", "steps"] = field(
        default="no",
        metadata={"help": "The checkpoint save strategy to use."},
    )
    save_steps: float = field(
        default=500,
        metadata={
            "help": (
                "Save checkpoint every X updates steps. Should be an integer or a float in range `[0,1)`. "
                "If smaller than 1, will be interpreted as ratio of total training steps."
            )
        },
    )
    save_total_limit: Optional[int] = field(
        default=1,
        metadata={
            "help": (
                "If a value is passed, will limit the total amount of checkpoints. Deletes the older checkpoints in"
                " `output_dir`. When `load_best_model_at_end` is enabled, the 'best' checkpoint according to"
                " `metric_for_best_model` will always be retained in addition to the most recent ones. For example,"
                " for `save_total_limit=5` and `load_best_model_at_end=True`, the four last checkpoints will always be"
                " retained alongside the best model. When `save_total_limit=1` and `load_best_model_at_end=True`,"
                " it is possible that two checkpoints are saved: the last one and the best one (if they are different)."
                " Default is unlimited checkpoints"
            )
        },
    )
    save_only_model: bool = field(
        default=True,
        metadata={
            "help": (
                "When checkpointing, whether to only save the model, or also the optimizer, scheduler & rng state."
                "Note that when this is true, you won't be able to resume training from checkpoint."
                "This enables you to save storage by not storing the optimizer, scheduler & rng state."
                "You can only load the model using from_pretrained with this option set to True."
            )
        },
    )
    per_device_train_batch_size: int = field(
        default=4, metadata={"help": "Batch size per GPU/TPU/MPS/NPU core/CPU for training."}
    )
    per_device_eval_batch_size: int = field(
        default=4, metadata={"help": "Batch size per GPU/TPU/MPS/NPU core/CPU for evaluation."}
    )
    deepspeed: Optional[Union[dict, str]] = field(
        default=None,
        metadata={
            "help": (
                "Enable deepspeed and pass the path to deepspeed json config file (e.g. `ds_config.json`) or an already"
                " loaded json file as a dict"
            )
        },
    )
    ddp_find_unused_parameters: Optional[bool] = field(
        default=None,
        metadata={
            "help": (
                "When using distributed training, the value of the flag `find_unused_parameters` passed to "
                "`DistributedDataParallel`."
            )
        },
    )
    logging_steps: float = field(
        default=10,
        metadata={
            "help": (
                "Log every X updates steps. Should be an integer or a float in range `[0,1)`. "
                "If smaller than 1, will be interpreted as ratio of total training steps."
            )
        },
    )
    optim: Literal["adamw_torch", "sgd", "rmsprop", "adagrad"] = field(
        default='adamw_torch',
        metadata={"help": "The optimizer to use."},
    )
    seed: int = field(
        default=42,
        metadata={"help": "Random seed to be used with data loaders."},
    )
    do_train: bool = field(default=True, metadata={"help": "Whether to run training."})
    predict_with_generate : bool = field(default=False, metadata={"help": "Whether to run eval generate."})
    do_eval: bool = field(default=False, metadata={"help": "Whether to run eval."})
def parameterToLower(args_dict:Dict[str, Any]) -> Dict[str, Any]:
    args_env: Optional[Dict[str, Any]] = {}
    for key, _ in args_dict.items():
        env_var = os.environ.get(key)
        if env_var is not None:
            args_env[key.lower()] = os.environ[key]
    return args_env

def convert_to_correct_type(args):
    def str2bool(v):
        if isinstance(v, bool):
            return v
        if v.lower() in ('yes','true'):
            return True
        elif v.lower() in ('no','false'):
            return False
        
    fields = vars(args)
    converted_args = {}
    for field_name, value in fields.items():
        field_type = type(args).__dataclass_fields__[field_name].type
        if isinstance(value, str):
            if field_type is int:
                converted_args[field_name] = int(value)
            elif field_type is float:
                converted_args[field_name] = float(value)
            elif field_type is bool:
                converted_args[field_name] = str2bool(value)
            else:
                converted_args[field_name] = value
        else:
            converted_args[field_name] = value
    return type(args)(**converted_args)

def parseEnv() -> Dict[str, Any]:
    from transformers import HfArgumentParser
    logger.info(f"args_env_dict:{args_env_dict}")
    args_env = parameterToLower(args_env_dict)
    logger.info(f"args_env:{args_env}")

    parser = HfArgumentParser((PluginArguments,DataArguments,FinetuningArguments,ModelArguments,TrainingArguments))
    plugin_args, data_args, finetune_args, model_args, train_args = parser.parse_dict(args_env)
    plugin_args = convert_to_correct_type(plugin_args)
    logger.info(f"plugin args:{plugin_args}")

    data_args = convert_to_correct_type(data_args)
    finetune_args = convert_to_correct_type(finetune_args)
    model_args = convert_to_correct_type(model_args)
    train_args = convert_to_correct_type(train_args)
    return plugin_args, data_args, finetune_args, model_args, train_args
