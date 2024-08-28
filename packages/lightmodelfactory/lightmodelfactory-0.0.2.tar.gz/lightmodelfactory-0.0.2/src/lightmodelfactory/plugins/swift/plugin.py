import os,json
from typing import Callable
from lightmodelfactory.plugins.plugin import PLUGIN
from lightmodelfactory.plugins.plugin_build import PluginRg
from lightmodelfactory.util.logger import logger
from lightmodelfactory.plugins.swift.read_progress import FileMonitorThread
import shutil
import re


ERROR_LOG_PATH = './error.log'

@PluginRg.register('swift')
class SWIFT_PLUGIN(PLUGIN):
    def __init__(self) -> None:
        pass

    def preprocess(self):
        self.train_args.num_train_epochs = int(self.train_args.num_train_epochs)

    def get_dataset_path(self):
        dataset_desc_str = json.loads(self.plugin_args.dataset_desc)
        file_name = dataset_desc_str.get(self.data_args.dataset)
        dataset_path = file_name.get('file_name')
        return dataset_path

    def remove_field_value(self, input_str, field_name):
        pattern = rf'({field_name} [^\s]+)'
        result = re.sub(pattern, '', input_str)
        result = result.strip()
        result = re.sub(r'\s+', ' ', result)
        return result

    def delete_unnecessary_parameters(self, cmd):
        #['--bf16', 'False', '--fp16', 'True', '--overwrite_output_dir', 'True', '--do_train', 'True']
        pattern = "--bf16"
        modified_string = self.remove_field_value(cmd, pattern)

        pattern = "--fp16"
        modified_string = self.remove_field_value(modified_string, pattern)

        pattern = "--overwrite_output_dir"
        modified_string = self.remove_field_value(modified_string, pattern)

        pattern = "--do_train"
        modified_string = self.remove_field_value(modified_string, pattern)
        return modified_string

    def get_cmd(self):
        from lightmodelfactory.util.other import dataclass_to_cli_args
        cmd = f'swift sft \
            --model_type {self.plugin_args.pretrained_model_name} \
            --model_id_or_path {self.model_args.model_name_or_path} \
            --dataset {self.get_dataset_path()} \
            --output_dir {self.train_args.output_dir} \
            --sft_type lora '
        
        item_cmd = dataclass_to_cli_args(self.train_args)
        cmd += item_cmd

        logger.info(f'temp cmd : {cmd}')

        filter_cmd = self.delete_unnecessary_parameters(cmd)
        
        nproc_per_node = int(self.plugin_args.nproc_per_node)
        if nproc_per_node > 1:
            cuda_visible_devices = ','.join(str(i) for i in range(nproc_per_node))
            env_var_string = f"NPROC_PER_NODE={nproc_per_node} CUDA_VISIBLE_DEVICES={cuda_visible_devices} "
            result_cmd = env_var_string + filter_cmd

            logger.info(f'result_cmd : {result_cmd}')
            return result_cmd
        else:
            logger.info(f'filter_cmd : {filter_cmd}')
            return filter_cmd
        
    def start_train(self,train_progress:Callable):
        if self.train_args.overwrite_output_dir:
            if os.path.exists(self.train_args.output_dir) and os.path.isdir(self.train_args.output_dir):
                shutil.rmtree(self.train_args.output_dir)
        self.start_report_progress(train_progress)

        import subprocess
        error_file = open(f'{self.train_args.output_dir}/{ERROR_LOG_PATH}','w')
        process = subprocess.Popen(self.get_cmd(), 
                                stdout=None, 
                                stderr=error_file, 
                                text=True,
                                env=os.environ,
                                shell=True)
        
        process.wait()
        error_file.close()
        return process

    #root_dir：/home/swift/output/
    #在logging.jsonl在/home/swift/output/qwen2-7b-instruct/v0-20240712-103822/中
    #需要移到/home/swift/output/qwen2-7b-instruct/v0-20240712-103822/checkpoint-3150/
    def adjust_output_dir(self, root_dir):
        moved = False
        for dirpath, dirnames, filenames in os.walk(root_dir):
            for dirname in dirnames:
                if dirname.startswith("checkpoint-"):
                    checkpoint_dir = os.path.join(dirpath, dirname)
                    
                    files_to_move = ["logging.jsonl", "sft_args.json", "training_args.json"]
                    
                    for file_name in files_to_move:
                        src_file = os.path.join(dirpath, file_name)
                        
                        if os.path.exists(src_file):
                            dest_file = os.path.join(checkpoint_dir, file_name)
                            
                            shutil.move(src_file, dest_file)
                            logger.info(f"Moved {src_file} to {dest_file}")
                            moved = True
                    
                    if moved:
                        logger.info(f"move logging.jsonl suc, checkpoint_dir:{checkpoint_dir}")
                        return checkpoint_dir
        return None

    def move_path(self, root_dir):
        for subdir, dirs, files in os.walk(root_dir):
            for dirname in dirs:
                if dirname.startswith("checkpoint-"):
                    checkpoint_dir = os.path.join(subdir, dirname)
                    # 拷贝checkpoint-目录下的所有文件到根目录
                    for file_name in os.listdir(checkpoint_dir):
                        full_file_name = os.path.join(checkpoint_dir, file_name)
                        if os.path.isfile(full_file_name):
                            shutil.copy(full_file_name, root_dir)
                            logger.info(f"copy file_name:{file_name}, to root_dir:{root_dir}")
                    
                    # 删除上一级目录
                    lastdir = os.path.dirname(subdir)
                    logger.info(f"move lastdir:{lastdir}")
                    shutil.rmtree(lastdir)
                    break

    def train_postprocess(self):
        local_rank = int(os.environ.get("LOCAL_RANK", 0))
        end_to_zip = self.plugin_args.end_to_zip
        output_dir = self.adjust_output_dir(self.train_args.output_dir)
        if output_dir is None :
            logger.warning("output_dir is empty, save zip failed")
            return

        def create_zip_and_delete_folder(folder_path, zip_path):
            import os,zipfile,shutil
            try:
                files_to_compress = ['adapter_model.bin', 'adapter_config.json', 'pytorch_lora_weights.safetensors', 'adapter_model.safetensors']  # 要压缩的文件列表

                # 创建一个 ZIP 文件并添加文件到其中
                with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for file_name in files_to_compress:
                        file_path = os.path.join(folder_path, file_name)
                        if os.path.exists(file_path):
                            zipf.write(file_path, os.path.basename(file_path))

                # 删除 checkpoint-* 文件
                for dirpath, dirnames, filenames in os.walk(folder_path):
                    for dirname in dirnames:
                        if dirname.startswith("checkpoint-"):
                            dir_to_delete = os.path.join(dirpath, dirname)
                            logger.info(f"Deleting directory: {dir_to_delete}")
                            shutil.rmtree(dir_to_delete)
                
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

            self.move_path(self.train_args.output_dir)

    def get_token(self):
        from lightmodelfactory.util.calc_token import calc_tokens
        token_cnt = calc_tokens(self.data_args.dataset, self.plugin_args.dataset_desc, self.model_args.model_name_or_path)
        return token_cnt
        
    def get_error(self):
        import re
        from lightmodelfactory.util.parse_error import match_error_msg,ErrorType,ErrorCode
        with open(f'{self.train_args.output_dir}/{ERROR_LOG_PATH}', 'r') as file:
            for line in file:
                for attr_name, attr_value in vars(ErrorType).items():
                    if attr_name.startswith('error_type_'):
                        error_type_pattern = re.compile(attr_value)
                        match = re.search(error_type_pattern, line)
                        if match:
                            #print(f'match error_type_pattern {error_type_pattern},line {line}')
                            error_msg = match[1]
                            error_code = match_error_msg(error_msg)
                            return error_code,error_msg
            return ErrorCode.error_unknown,""

    def start_report_progress(self,train_progress_cb:Callable):
        self.file_monitor_thread = FileMonitorThread(self.train_args.output_dir, train_progress_cb)
        self.file_monitor_thread.start()

    def stop_report_progress(self):
        self.file_monitor_thread.stop()
        self.file_monitor_thread.join()

    def stop_train(self):
        self.stop_report_progress()