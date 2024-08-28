import json
import os
import subprocess
from typing import Callable

from lightmodelfactory.data.data_utils import write_val_dataset
from lightmodelfactory.plugins.plugin import PLUGIN
from lightmodelfactory.plugins.plugin_build import PluginRg
from lightmodelfactory.util.check_machine import is_npu, check_tool, get_file_format
from lightmodelfactory.util.logger import logger
from lightmodelfactory.data.loader import _get_merged_dataset_attrs,_get_merged_dataset
from lightmodelfactory.util.parse_error import match_error_msg, ErrorType, ErrorCode

ERROR_LOG_PATH = 'spark_error.log'

PACK_TOOL = "/spark_tools/packdata"  # 容器内位置
SFT_TRAIN = "/spark_tools/sparktrainer_sft"  # 容器内位置
LORA_TRAIN = "/spark_tools/sparktrainer_lora"  # 容器内位置

TEMP_DS = "/lmf/run"
LMDB_FILE = "/lmf/run/lmdb.json"
SparkTemplate = '''### Instruction: {system}'''

STEP_LIST = ["data_transform", "pack_data", "train"]


@PluginRg.register('spark')
class SPARK_PLUGIN(PLUGIN):
    def __init__(self) -> None:
        self.is_npu = is_npu()
        logger.info(f"Spark Plugin Loaded in npu: {self.is_npu} machine...")

    def prepare_spark_tools(self):
        tools_map = {}
        tools = [PACK_TOOL]
        if self.finetune_args.finetuning_type == "full":
            tools.append(SFT_TRAIN)
        elif self.finetune_args.finetuning_type == "lora":
            tools.append(LORA_TRAIN)
        for t in tools:
            if not check_tool(t):
                raise Exception(f"not find {t}")

        tools_map['pack'] = PACK_TOOL
        tools_map['sft_train'] = SFT_TRAIN
        tools_map['lora_train'] = LORA_TRAIN
        return tools_map

    def preprocess(self):
        dir = os.path.dirname(os.path.abspath(__file__))
        logger.info(f"datasets desc {self.plugin_args.dataset_desc}")

        logger.info(f"data_args {self.data_args}")
        logger.info(f"train_args {self.train_args}")
        logger.info(f"finetune_args {self.finetune_args}")

    def get_token(self):
        pass

    def get_error(self):
        pass

    def get_lr(self):
        return "[1.6e-6]"

    def get_model_arch(self):
        self.plugin_args.pretrained_model_name = self.plugin_args.pretrained_model_name.replace("_", "-")
        if self.plugin_args.pretrained_model_name == "spark-13b-6k-taoyun":
            return '13Bv2'
        elif self.plugin_args.pretrained_model_name == "spark-2.6b-lingsi":
            return '2.6B'
        elif self.plugin_args.pretrained_model_name == "spark-tiny":
            return '1.3B'
        elif self.plugin_args.pretrained_model_name == "spark-mini":
            return '2.6B'
        elif self.plugin_args.pretrained_model_name == "spark-lite":
            return '13B'

    def get_runner_cmd(self):
        NNODES = 1
        RANK = 0
        NPROC_PER_NODE = 1
        PORT = 4525
        MAST_ADDR = "127.0.0.1"
        is_lora = False
        DIST_ARGS = f"--master_addr={MAST_ADDR} --master_port={PORT} --nnodes={NNODES} --node_rank={RANK} --nproc_per_node={NPROC_PER_NODE}"
        if self.finetune_args.finetuning_type == "lora":
            is_lora = True

        TRAIN_TOOL = LORA_TRAIN if is_lora else SFT_TRAIN
        lr = self.get_lr()
        MaxEpoch = int(self.train_args.num_train_epochs)
        MODEARCH = self.get_model_arch()
        full_op = "true" if not is_lora else "false"
        TORCH_CMD = (f'torchrun --no_python {DIST_ARGS} {TRAIN_TOOL} '
                     f'hydra.run.dir="/lmf/run/checkpoints" '
                     f'common.license_dir=/lmf/license '
                     f'common.log_file=/lmf/run/log/train.log '
                     f'dataset.train_subset={LMDB_FILE} '
                     f'dataset.valid_subset={LMDB_FILE} '
                     f'model.from_pretrained=/models/P1T1V1/ '
                     f'optimization.lr={lr} '
                     f'model_parallel.num_micro_batch=1 '
                     f'model_parallel.micro_batch_size=1 '
                     f'model_parallel.tensor_model_parallel_size=1 '
                     f'model_parallel.pipeline_model_parallel_size=1 '
                     f'checkpoint.save_interval_updates=5000 '
                     f'dataset.validate_interval_updates=500 '
                     f'optimization.max_epoch={MaxEpoch} '
                     f'model_parallel.recompute_granularity=full '
                     f'checkpoint.full_op_of_inference_engine={full_op} '
                     f'common.model_arch={MODEARCH} '
                     )
        if is_lora:
            TORCH_CMD += " checkpoint.model_paralle_size_of_inference_engine=1"
        logger.info(f'CMD: {TORCH_CMD}')
        return (f'bash -c "source /usr/local/Ascend/ascend-toolkit/set_env.sh\n' +
                f'{TORCH_CMD}"')

    def get_pack_cmd(self, target_dataset):
        # 执行打包命令
        RUN_PACK_CMD = '{pack_tool} -input "{jsonl_file}" \
                        -output "/lmf/run/packed_data" \
                        --data-type "{finetuned_data_type}" \
                        --tokenizer "/lmf/vocab.bin" \
                        --license-dir /lmf/license \
                        --model-version "spark-v2.0.0-20230815"'
        stage = self.finetune_args.stage
        stage = "sft"
        cmd = RUN_PACK_CMD.format(pack_tool=PACK_TOOL, finetuned_data_type=stage, jsonl_file=target_dataset)
        return cmd

    def preprocess_dataset(self):
        os.makedirs(TEMP_DS, exist_ok=True)
        tools = self.prepare_spark_tools()
        packaged_ds = '/lmf/run/packed_data/packed_data.json'
        dataset_desc = json.loads(self.plugin_args.dataset_desc)
        datasets_attrs = _get_merged_dataset_attrs(self.data_args.dataset, self.data_args, dataset_desc, self.finetune_args.stage)
        dataset = _get_merged_dataset(self.data_args.dataset, self.data_args, dataset_desc, self.finetune_args.stage, self.train_args)
        write_val_dataset(dataset,self.data_args, self.train_args.seed )
        logger.info("Val Dataset wrote Done ...")

        target_dataset = os.path.join(TEMP_DS, "final_dataset.jsonl")
        if os.path.exists(packaged_ds):
            logger.info("Existing  packed dataset, Skip Packing..")
            return
        with open(target_dataset, "w") as ds:
            for da in datasets_attrs:
                logger.info(f"processing dataset {da.dataset_name}")
                self.process_single_dataset(da, ds)
        # 打包
        cmd = self.get_pack_cmd(target_dataset)
        logger.info(f"Starting  Packing Spark {self.finetune_args.stage} Dataset")
        subprocess.call(cmd, shell=True)
        logger.info(f"End  Packing ...")

        self.gen_lmdb(packaged_ds)

    def process_single_dataset(self, dataset_attr, target_fp):
        filename = dataset_attr.dataset_name
        exists, _fmt = get_file_format(filename)
        if not exists:
            self.metrics_server.report_error(ErrorCode.error_dataset_no_found, str("No such dataset"))
            raise FileNotFoundError(str("No such dataset"))
        if _fmt == "jsonl":
            self.read_jsonl_file(dataset_attr, filename, target_fp)
        elif _fmt == "json":
            self.read_json_file(dataset_attr, filename, target_fp)
        logger.info("Extracted alpaca intput  to {}".format(target_fp.name))

    def read_jsonl_file(self, ds_attr, inpt_file_name, out_fp):
        with open(inpt_file_name, 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                json_line = json.loads(line)
                converted_map = {}
                if ds_attr.formatting == "alpaca":
                    converted_map["input"] = json_line[ds_attr.prompt]
                    converted_map['target'] = json_line[ds_attr.response]
                    out_fp.write(json.dumps(converted_map, ensure_ascii=False) + "\n")
                elif ds_attr.formatting == "sharegpt":
                    self.do_share_gpt_item(json_line, ds_attr, converted_map, out_fp)

    def read_json_file(self, ds_attr, inpt_file_name, out_fp):
        with open(inpt_file_name, 'r') as f:
            lines = json.load(f)
            for line in lines:
                json_line = line
                converted_map = {}
                if ds_attr.formatting == "alpaca":
                    converted_map["input"] = json_line[ds_attr.prompt]
                    converted_map['target'] = json_line[ds_attr.response]
                    out_fp.write(json.dumps(converted_map, ensure_ascii=False) + "\n")
                elif ds_attr.formatting == "sharegpt":
                    self.do_share_gpt_item(json_line, ds_attr, converted_map, out_fp)

    def gen_lmdb(self, data_json="/sparksfly/data/data.json"):
        lmdb = {
            "file_type": "LMDB",
            "dataset": [
                {
                    "lm_token": data_json,
                    "range": [
                        0,
                        0
                    ],
                    "meta": {
                        "chunk_sample_rate": 1
                    }
                }
            ]
        }
        # 实际这里可能需要区分 训练集 验证集 lmdb
        with open(LMDB_FILE, 'w') as t:
            json.dump(lmdb, t)
        logger.info(f"gen {LMDB_FILE}  success...")

    def do_share_gpt_item(self, json_line: dict, ds_attr, converted_map, out_fp) -> None:
        one_turn = {}
        for ms in json_line[ds_attr.messages]:
            # 这里暂时没有考虑多轮数据
            if ms[ds_attr.role_tag] == ds_attr.user_tag:
                if "input" in one_turn:
                    # 这里如果input已经在里面说明 多轮第二次input了 直接忽略后续
                    break
                one_turn["input"] = ms[ds_attr.content_tag]
            elif ms[ds_attr.role_tag] == ds_attr.assistant_tag:
                one_turn["assistant"] = ms[ds_attr.content_tag]
            elif ms[ds_attr.role_tag] == ds_attr.function_tag:
                one_turn["function_call"] = ms[ds_attr.content_tag]
        system = ""
        if ds_attr.system and ds_attr.system in json_line:
            system = json_line[ds_attr.system]
        elif ds_attr.system is None and "system" in json_line:
            system = json_line["system"]
        tools = None
        if ds_attr.tools and ds_attr.tools in json_line:
            tools = json_line[ds_attr.tools]
        elif ds_attr.tools is None and "tools" in json_line:
            tools = json_line['tools']

        if tools:
            converted_map["input"] = SparkTemplate.format(
                system=system) + "\n ###TOOLS: \n " + tools + "\n###INPUT \n" + \
                                     one_turn['input']
        else:
            converted_map["input"] = SparkTemplate.format(system=system) + "\n###INPUT \n" + \
                                     one_turn['input']
        if "function_call" in one_turn:
            converted_map['target'] = one_turn['function_call']
        elif "assistant" in one_turn:
            converted_map['target'] = one_turn["assistant"]

        out_fp.write(json.dumps(converted_map, ensure_ascii=False) + "\n")

    def write_dataset_info(self, dataset_desc: str):
        import json, os
        os.makedirs('./data', exist_ok=True)
        data_to_write = json.loads(dataset_desc)
        output_json_file = './data/dataset_info.json'
        with open(output_json_file, 'w', encoding='utf-8') as f:
            json.dump(data_to_write, f, ensure_ascii=False, indent=4)

    def start_train(self, train_progress: Callable):
        os.makedirs(self.train_args.output_dir, exist_ok=True)
        self.preprocess_dataset()
        # self.start_report_progress(train_progress)
        if self.is_npu:
            pass
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

    def stop_train(self):
        pass

    def train_postprocess(self):
        pass

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
