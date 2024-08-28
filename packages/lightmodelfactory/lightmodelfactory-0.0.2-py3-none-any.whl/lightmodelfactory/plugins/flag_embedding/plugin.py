import os,json,shutil
from typing import Callable
from lightmodelfactory.plugins.plugin import PLUGIN
from lightmodelfactory.plugins.plugin_build import PluginRg
from lightmodelfactory.util.logger import logger

ERROR_LOG_PATH = './error.log'

class embedding_model_type(object):
    bge_m3_type = 'BGE_M3'
    reranker_type = 'reranker'

@PluginRg.register('embedding')
class FLAG_EMBEDDING_PLUGIN(PLUGIN):
    def __init__(self) -> None:
        pass

    def preprocess(self):
        deepspeed_dir = os.path.dirname(os.path.abspath(__file__))
        deepspeed_dir = os.path.join(deepspeed_dir,"../ds_zero2_no_offload.json")
        self.train_args.ddp_find_unused_parameters = False
        self.train_args.deepspeed = deepspeed_dir
        self.train_args.save_strategy = 'no'
        logger.info(f'self.plugin_args {self.plugin_args}')

    def get_token(self):
        from lightmodelfactory.util.calc_token import calc_tokens
        token_cnt = calc_tokens(self.data_args.dataset, self.plugin_args.dataset_desc, self.model_args.model_name_or_path)
        return token_cnt  

    def get_error(self):
        import re
        from lightmodelfactory.util.parse_error import match_error_msg,ErrorType,ErrorCode
        with open(ERROR_LOG_PATH, 'r') as file:
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
        
    def get_dataset_path(self):
        dataset_desc_str = json.loads(self.plugin_args.dataset_desc)
        file_name = dataset_desc_str.get(self.data_args.dataset)
        dataset_path = file_name.get('file_name')
        return dataset_path

    def get_bge_m3_cmd(self):
        from lightmodelfactory.util.other import get_port,dataclass_to_cli_args
        listen_port_start = get_port(29500)
        cmd = f'torchrun --nproc_per_node {self.plugin_args.nproc_per_node} --master_port {listen_port_start} \
            -m FlagEmbedding.BGE_M3.run \
            --model_name_or_path {self.model_args.model_name_or_path} \
            --train_data {self.get_dataset_path()} \
            --dataloader_drop_last True \
            --normlized True \
            --temperature 0.02 \
            --query_max_len {int(self.data_args.cutoff_len)//2} \
            --passage_max_len {int(self.data_args.cutoff_len)//2} \
            --train_group_size 2 \
            --negatives_cross_device \
            --logging_steps 10 \
            --same_task_within_batch True \
            --unified_finetuning True \
            --use_self_distill True '
        
        item_cmd = dataclass_to_cli_args(self.train_args)
        cmd += item_cmd
        logger.info(f'get_bge_m3_cmd : {cmd}')
        return cmd

    def get_reranker_cmd(self):
        from lightmodelfactory.util.other import get_port,dataclass_to_cli_args
        listen_port_start = get_port(29500)
        cmd = f'torchrun --nproc_per_node {self.plugin_args.nproc_per_node} --master_port {listen_port_start} \
            -m FlagEmbedding.reranker.run \
            --model_name_or_path {self.model_args.model_name_or_path} \
            --train_data {self.get_dataset_path()} \
            --dataloader_drop_last True \
            --train_group_size 16 \
            --max_len {self.data_args.cutoff_len} '
        
        item_cmd = dataclass_to_cli_args(self.train_args)
        cmd += item_cmd
        logger.info(f'get_bge_m3_cmd : {cmd}')
        return cmd

    def get_runner_cmd(self):
        model_name = self.plugin_args.pretrained_model_name

        def get_embedding_model_type(filename,model_name):
            with open(filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
            type = data.get(model_name,None)
            return type

        dir = os.path.dirname(os.path.abspath(__file__))
        template_json = os.path.join(dir,"embedding_type.json")
        type = get_embedding_model_type(template_json, model_name)
        if type is None:
            raise ValueError(f'model_name not support {model_name}')
        if type == embedding_model_type.bge_m3_type:
            return self.get_bge_m3_cmd()
        elif type == embedding_model_type.reranker_type:
            return self.get_reranker_cmd()

    def start_train(self,train_progress:Callable):
        if self.train_args.overwrite_output_dir:
            if os.path.exists(self.train_args.output_dir) and os.path.isdir(self.train_args.output_dir):
                shutil.rmtree(self.train_args.output_dir)

        import subprocess
        error_file = open(ERROR_LOG_PATH,'w')
        process = subprocess.Popen(self.get_runner_cmd(), 
                                stdout=None, 
                                stderr=error_file, 
                                text=True,
                                env=os.environ,
                                shell=True)
        
        process.wait()
        error_file.close()
        return process
    
    def stop_train(self):
        pass

    def train_postprocess(self):
        pass