import os, json
import subprocess
from typing import Callable

from lightmodelfactory.data.loader import _get_merged_dataset_attrs, _get_merged_dataset
from lightmodelfactory.plugins.plugin import PLUGIN
from lightmodelfactory.plugins.plugin_build import PluginRg
from lightmodelfactory.util.logger import logger
from lightmodelfactory.plugins.llama_factory.read_progress import FileMonitorThread
import shutil
from lightmodelfactory.data.data_utils import write_val_dataset,EVAL_DATASET


def load_json_file(filename='model_template.json'):
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def find_model_value_by_default(data, key, default):
    return data.get(key, default)


ERROR_LOG_PATH = 'error.log'


@PluginRg.register('llama_factory')
class FACTORY_PLUGIN(PLUGIN):
    def __init__(self) -> None:
        pass

    def update_algorithms_dict(self):
        if self.finetune_args.use_galore:
            subprocess.check_call("pip install galore-torch", shell=True)
            self.train_args.bf16 = True
            self.train_args.fp16 = False
            self.finetune_args.pure_bf16 = True
            self.train_args.per_device_train_batch_size = 1
            if self.data_args.cutoff_len > '1024':
                logger.warning('GaLore max cutoff_len > 1024,set to 1024')
                self.data_args.cutoff_len = 1024
        if self.finetune_args.use_badam:
            subprocess.check_call("pip install badam", shell=True)
            self.train_args.bf16 = True
            self.train_args.fp16 = False
            self.finetune_args.pure_bf16 = True
        if self.finetune_args.stage == 'dpo':
            self.train_args.per_device_eval_batch_size = 1
            self.data_args.cutoff_len = 1024
        if self.finetune_args.stage == 'orpo':
            self.finetune_args.stage = 'dpo'
            self.finetune_args.pref_loss = 'orpo'
        if self.finetune_args.stage == 'simpo':
            self.finetune_args.stage = 'dpo'
            self.finetune_args.pref_loss = 'simpo'

    def preprocess(self):
        dir = os.path.dirname(os.path.abspath(__file__))
        template_json = os.path.join(dir, "model_template.json")
        lora_target_json = os.path.join(dir, "model_lora_target.json")
        templates = load_json_file(template_json)
        template = find_model_value_by_default(templates, self.plugin_args.pretrained_model_name, 'empty')
        self.data_args.template = template
        lora_targets = load_json_file(lora_target_json)
        lora_target = find_model_value_by_default(lora_targets, self.plugin_args.pretrained_model_name, 'q_proj,v_proj')
        self.finetune_args.lora_target = lora_target

        ## 数据集信息，以及添加eval数据集
        self.write_or_update_dataset_info(self.plugin_args.dataset_desc)
        eval_ds_path = self.preprocess_eval_dataset()
        self.write_or_update_dataset_info(self.plugin_args.dataset_desc, eval_ds_path)

        if self.model_args.quantization_bit != 4:
            self.model_args.quantization_bit = None
        self.update_algorithms_dict()
        logger.info(f"data_args {self.data_args}")
        logger.info(f"train_args {self.train_args}")
        logger.info(f"finetune_args {self.finetune_args}")

    def preprocess_eval_dataset(self, dataset_desc):
        dataset = _get_merged_dataset(self.data_args.dataset, self.data_args, dataset_desc, self.finetune_args.stage)
        ds = write_val_dataset(dataset, self.data_args, self.train_args.seed)
        logger.info(f"eval dataset wrote successfully: ./data/eval.jsonl ")
        return ds
    def support_deepspeed(self):
        if self.model_args.use_unsloth or self.finetune_args.use_badam or self.finetune_args.use_galore:
            return False
        if self.finetune_args.stage == 'dpo':
            return False
        return True

    def get_runner_cmd(self):
        if self.plugin_args.use_fsdp:
            return self.get_fsdp_cmd()

        args = []
        args_front_ddp = ['FORCE_TORCHRUN=1']
        args_mid = ['llamafactory-cli', 'train']
        from lightmodelfactory.util.other import get_port, dataclass_to_cli_args
        if self.support_deepspeed():
            deepspeed_dir = os.path.dirname(os.path.abspath(__file__))
            deepspeed_dir = os.path.join(deepspeed_dir, "../ds_zero2_no_offload.json")
            self.train_args.ddp_find_unused_parameters = False
            self.train_args.deepspeed = deepspeed_dir

            listen_port_start = get_port(29500)
            args_front_ddp.append(f'NPROC_PER_NODE={self.plugin_args.nproc_per_node} MASTER_PORT={listen_port_start}')
            args += args_front_ddp
            args += args_mid
        else:
            args += args_mid
        # 处理 val_size
        if self.data_args.val_size > 1e-6:
            logger.info(f"we have used val size to split evaluation dataset: {self.data_args.val_size}, now disable it ")
            self.data_args.val_size = 0.0
            self.train_args.do_eval = True
            self.train_args.predict_with_generate = True
            self.data_args.eval_dataset = EVAL_DATASET


        for item in self.data_args, self.model_args, self.finetune_args, self.train_args:
            item_cmd = dataclass_to_cli_args(item)
            args.append(item_cmd)
        cmd = " ".join(args)
        logger.info(f'run cmd {cmd}')
        return cmd

    def modify_fsdp_config_yaml(self, fsdp_config_path: str):
        import yaml
        with open(fsdp_config_path, 'r') as file:
            data = yaml.safe_load(file)
        data['num_processes'] = self.plugin_args.nproc_per_node
        with open(fsdp_config_path, 'w') as file:
            yaml.dump(data, file, default_flow_style=False)

    def get_fsdp_cmd(self):
        def get_package_install_path(package_name):
            import importlib.util
            try:
                module_spec = importlib.util.find_spec(package_name)
                if module_spec is None:
                    raise ModuleNotFoundError(f"Package {package_name} not found.")
                return os.path.dirname(module_spec.origin)
            except ModuleNotFoundError as e:
                raise

        cur_dir = os.path.dirname(os.path.abspath(__file__))
        fsdp_config_dir = os.path.join(cur_dir, "fsdp_config.yaml")
        self.modify_fsdp_config_yaml(fsdp_config_dir)
        llama_factory_install_path = get_package_install_path('llamafactory')
        subprocess.check_call("pip install bitsandbytes==0.43.0", shell=True)
        cmd = f'accelerate launch --config_file {fsdp_config_dir} \
            {llama_factory_install_path}/../train.py '

        self.model_args.quantization_bit = 4
        args = []
        for item in self.data_args, self.model_args, self.finetune_args, self.train_args:
            from lightmodelfactory.util.other import dataclass_to_cli_args
            item_cmd = dataclass_to_cli_args(item)
            args.append(item_cmd)
        cmd += " ".join(args)
        logger.info(f'run fsdp cmd {cmd}')
        return cmd

    def start_train(self, train_progress: Callable):
        os.makedirs(self.train_args.output_dir, exist_ok=True)
        self.start_report_progress(train_progress)

        error_file = open(f'{self.train_args.output_dir}/{ERROR_LOG_PATH}', 'w')
        # process = subprocess.run(self.get_runner_cmd(), stderr=error_file, shell=True)
        process = subprocess.Popen(self.get_runner_cmd(),
                                   stdout=None,
                                   stderr=error_file,
                                   text=True,
                                   env=os.environ,
                                   shell=True)

        process.wait()
        error_file.close()
        return process

    def train_postprocess(self):
        local_rank = int(os.environ.get("LOCAL_RANK", 0))
        end_to_zip = self.plugin_args.end_to_zip
        output_dir = self.train_args.output_dir

        def create_zip_and_delete_folder(folder_path, zip_path):
            import os, zipfile, shutil
            try:
                files_to_compress = ['adapter_model.bin', 'adapter_config.json', 'pytorch_lora_weights.safetensors',
                                     'adapter_model.safetensors']  # 要压缩的文件列表

                # 创建一个 ZIP 文件并添加文件到其中
                with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for file_name in files_to_compress:
                        file_path = os.path.join(folder_path, file_name)
                        if os.path.exists(file_path):
                            zipf.write(file_path, os.path.basename(file_path))

                """
                # 删除 checkpoint-* 文件
                for dirpath, dirnames, filenames in os.walk(folder_path):
                    for dirname in dirnames:
                        if dirname.startswith("checkpoint-"):
                            dir_to_delete = os.path.join(dirpath, dirname)
                            logger.info(f"Deleting directory: {dir_to_delete}")
                            shutil.rmtree(dir_to_delete)
                """

                # 删除 runs 文件夹
                runs_folder = os.path.join(folder_path, "runs")
                if os.path.exists(runs_folder):
                    shutil.rmtree(runs_folder)

                logger.info(f"文件夹 '{folder_path}' 已打包为 '{zip_path}' 并删除其他文件")
            except Exception as e:
                logger.info(f"发生错误：{e}")

        if local_rank == 0 and end_to_zip:
            zip_file_path = output_dir + "/adapter.zip"
            create_zip_and_delete_folder(output_dir, zip_file_path)

        if self.plugin_args.merge_lora:
            def format_command(model_name_or_path, adapter_name_or_path, template, finetuning_type, export_dir):
                command = "llamafactory-cli export --model_name_or_path %s --adapter_name_or_path %s --template %s --finetuning_type %s --export_dir %s --export_device auto"
                return command % (model_name_or_path, adapter_name_or_path, template, finetuning_type, export_dir)

            cmd = format_command(self.model_args.model_name_or_path, output_dir,
                                 self.data_args.template, self.finetune_args.finetuning_type, output_dir)
            subprocess.run(cmd, shell=True)

    def get_token(self):
        from lightmodelfactory.util.calc_token import calc_tokens
        token_cnt = calc_tokens(self.data_args.dataset, self.plugin_args.dataset_desc,
                                self.model_args.model_name_or_path)
        return token_cnt

    def get_error(self):
        import re
        from lightmodelfactory.util.parse_error import match_error_msg, ErrorType, ErrorCode
        with open(f'{self.train_args.output_dir}/{ERROR_LOG_PATH}', 'r') as file:
            for line in file:
                for attr_name, attr_value in vars(ErrorType).items():
                    if attr_name.startswith('error_type_'):
                        error_type_pattern = re.compile(attr_value)
                        match = re.search(error_type_pattern, line)
                        if match:
                            # print(f'match error_type_pattern {error_type_pattern},line {line}')
                            error_msg = match[1]
                            error_code = match_error_msg(error_msg)
                            return error_code, error_msg
            return ErrorCode.error_unknown, ""

    def start_report_progress(self, train_progress_cb: Callable):
        self.file_monitor_thread = FileMonitorThread(self.train_args.output_dir, train_progress_cb)
        self.file_monitor_thread.start()

    def stop_report_progress(self):
        self.file_monitor_thread.stop()
        self.file_monitor_thread.join()

    def write_or_update_dataset_info(self, dataset_desc: str, eval_ds_file=None):
        os.makedirs('./data', exist_ok=True)
        data_to_write = json.loads(dataset_desc)
        if eval_ds_file:
            eval_dataset = EVAL_DATASET
            data_to_write[eval_dataset] = {"file_name": eval_ds_file}
        output_json_file = './data/dataset_info.json'
        with open(output_json_file, 'w', encoding='utf-8') as f:
            json.dump(data_to_write, f, ensure_ascii=False, indent=4)
        return output_json_file

    def stop_train(self):
        self.stop_report_progress()
