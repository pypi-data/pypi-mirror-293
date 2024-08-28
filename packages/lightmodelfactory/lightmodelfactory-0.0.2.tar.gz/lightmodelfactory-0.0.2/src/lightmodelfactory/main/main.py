import os,json,zipfile,shutil,subprocess
from typing import Any, Dict, Optional
from lightmodelfactory.util.parse_error import match_error_msg
from lightmodelfactory.util.logger import logger
from lightmodelfactory.plugins.plugin import PLUGIN
from lightmodelfactory.main.callback import HttpReportAgent
import traceback

agent_metrics:HttpReportAgent = None

def pack_dict_args() -> Dict[str, Any]:
    from lightmodelfactory.util.param import parseEnv
    return parseEnv()

def grab_error(msg):
    error_code = match_error_msg(msg)
    logger.error(f'msg: {msg}, error_code: {error_code}')
    return error_code,str(msg)

def start_http_report_agent(pretrained_model_name):
    global agent_metrics
    agent_metrics = HttpReportAgent(pretrained_model_name)
    agent_metrics.start()


def train_progess_cb(left_train_time, process,loss):
    global agent_metrics
    logger.info(f"set left_train_time:{left_train_time}, process:{process}, loss:{loss}")
    agent_metrics.set_params(left_train_time, loss,process)

def report_error(error_code,msg):
    global agent_metrics
    agent_metrics.report_error(error_code, str(msg))

def report_token(token_cnt):
    global agent_metrics
    agent_metrics.report_token(token_cnt)

def stop_report_agent():
    global agent_metrics
    agent_metrics.stop()

def run_train_script():
    plugin_args, data_args, finetune_args, model_args, train_args = pack_dict_args()
    plugin:PLUGIN = PLUGIN.build_plugin(plugin_args, data_args, finetune_args, model_args, train_args)
    global agent_metrics

    try:
        start_http_report_agent(plugin_args.pretrained_model_name)
        plugin.register_metrics_server(agent_metrics)
        token_cnt = plugin.get_token()
        report_token(token_cnt)

        plugin.preprocess()
        result = plugin.start_train(train_progess_cb)
        if result.returncode != 0:
            logger.error(f"train exited with error code {result.returncode}")
            error_code, msg = plugin.get_error()

            #fix cuda
            from lightmodelfactory.util.parse_error import ErrorCode
            if error_code == ErrorCode.error_machine_oom:
                msg = 'OOM'
                
            report_error(error_code, msg)
            plugin.stop_train()
            raise ValueError(f'train error_code {error_code}, msg {msg}')
        else:
            plugin.train_postprocess()
            stop_report_agent()
            plugin.stop_train()
            logger.info("train executed successfully.")
    except Exception as e:
        if e:
            error_code, msg = grab_error(e)
            report_error(error_code, msg)
        plugin.stop_train()
        traceback.print_exc()
        logger.error(f"Failed to run train: {e}")
        raise

if __name__ == "__main__":
    run_train_script()