"""
Helpers to support streaming generate output.
Borrowed from https://github.com/oobabooga/text-generation-webui/blob/ad37f396fc8bcbab90e11ecf17c56c97bfbd4a9c/modules/callbacks.py
"""

import traceback
from queue import Queue
from threading import Thread
import threading
import os
import requests
from datetime import datetime
import transformers
from transformers import TrainerCallback
from lightmodelfactory.util.logger import logger

class Stream(transformers.StoppingCriteria):
    def __init__(self, callback_func=None):
        self.callback_func = callback_func

    def __call__(self, input_ids, scores) -> bool:
        if self.callback_func is not None:
            self.callback_func(input_ids[0])
        return False


class Iteratorize:

    """
    Transforms a function that takes a callback
    into a lazy iterator (generator).
    """

    def __init__(self, func, kwargs={}, callback=None):
        self.mfunc = func
        self.c_callback = callback
        self.q = Queue()
        self.sentinel = object()
        self.kwargs = kwargs
        self.stop_now = False

        def _callback(val):
            if self.stop_now:
                raise ValueError
            self.q.put(val)

        def gentask():
            try:
                ret = self.mfunc(callback=_callback, **self.kwargs)
            except ValueError:
                pass
            except:
                traceback.print_exc()
                pass

            self.q.put(self.sentinel)
            if self.c_callback:
                self.c_callback(ret)

        self.thread = Thread(target=gentask)
        self.thread.start()

    def __iter__(self):
        return self

    def __next__(self):
        obj = self.q.get(True, None)
        if obj is self.sentinel:
            raise StopIteration
        else:
            return obj

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop_now = True

import time
class TrainProgress(TrainerCallback):
    def __init__(self, cb):
        self.start_time = time.time()
        self.cb = cb

    def on_train_begin(self, args, state, control, **kwargs):
        self.start_time = time.time()

    def on_step_end(self, args, state, control, **kwargs):
        cur_step = state.global_step
        max_step = state.max_steps
        process : float = cur_step * 100 // max_step

        if cur_step > 0:
            costed_time = time.time() - self.start_time
            predict_all_time = costed_time * max_step / cur_step
            remain_time = predict_all_time - costed_time

            if state.log_history:
                max_loss_entry = max(state.log_history, key=lambda x: x['step'])
                # 获取最大步数对应的 loss 值
                max_loss_value = max_loss_entry.get('loss',-1)
            else:
                max_loss_value = -1
               
        self.cb(self.start_time,costed_time,remain_time,process,max_loss_value)

class HttpReportAgent():
    def __init__(self,pretrain_name) -> None:
        self.start_train_time = time.time()
        self.left_train_time = -1
        self.loss = -1
        self.progress = -1
        self.pretrained_model_name = pretrain_name
        self.task_id = os.environ.get('TRAIN_ID')
        self.max_retries = 3
        self.url_progress = os.environ.get('URL_REPORT_PROGRESS')
        self.url_loss = os.environ.get('URL_REPORT_LOSS')
        self.url_error = os.environ.get('URL_REPORT_ERR')
        self.url_token = os.environ.get('URL_REPORT_TOKENS')
        self.interval = 30
        self.timer_thread = None
        self.running = False

        logger.info(f'URL_REPORT_PROGRESS {self.url_progress},URL_REPORT_LOSS {self.url_loss},URL_REPORT_ERR {self.url_error}')
    
    def make_http_request(self, post_data, url):
        if url is None:
            logger.error('METRICS_REPORT_URL failed')
            return
        
        retries = 0
        while retries < self.max_retries:
            try:
                headers = {'Content-Type': 'application/json'}
                requests.post(url, headers=headers,json=post_data, timeout=5)
                logger.info(f'make_http_request success url {url},data {post_data}')
                break
            except requests.Timeout:
                retries+=1


    def report_progress(self):
        if self.left_train_time == -1:
            return
        d = {
            "train_id":self.task_id,
            "pretrained_model_name": self.pretrained_model_name,       
            "left_train_time":int(self.left_train_time),                                       
            "start_train_time":int(self.start_train_time),
            "progress": int(self.progress)
        }

        self.make_http_request(d, self.url_progress)

    def report_loss(self):
        if self.loss == -1:
            return
        d = {
            "train_id":self.task_id,
            "pretrained_model_name": self.pretrained_model_name,       
            "report_time": int(time.time()),
            "loss": self.loss
        }

        self.make_http_request(d, self.url_loss)

    def report_error(self,error_code,error_info):
        if not self.running:
            return
        d = {
            "train_id":self.task_id,
            "pretrained_model_name": self.pretrained_model_name,
            "error_code":error_code,
            "error_info":error_info
        }
        self.make_http_request(d, self.url_error)
        self.stop()

    def report_token(self,token_cnt):
        if not self.running:
            logger.error(f'report_token not running')
            return
        d = {
            "train_id":self.task_id,
            "pretrained_model_name": self.pretrained_model_name,
            "tokens":token_cnt
        }
        self.make_http_request(d, self.url_token)

    def run_thread(self,internal):
        while self.running:
            self.report_loss()
            self.report_progress()
            time.sleep(internal)

    def test_url(self):
        import re
        pattern = re.compile(r'http://([\d.]+):(\d+)/')
        if self.url_progress is None:
            return False
        match = pattern.match(self.url_progress)
        if match:
            host = match.group(1)
            port = match.group(2)
            import socket
            try:
                socket.create_connection((host, port), timeout=5)
                logger.info(f"{host}:{port} is reachable.")
                return True
            except (socket.timeout, ConnectionError):
                logger.info(f"{host}:{port} is not reachable.")
                return False
        else:
            return False

    def start(self):
        import os
        local_rank = os.environ.get('LOCAL_RANK',0)
        if local_rank == 0 or local_rank == '0':
            if not self.test_url():
                return
            self.running = True
            self.timer_thread = threading.Thread(target=self.run_thread,args=(self.interval,))
            self.timer_thread.daemon = True
            self.timer_thread.start()

    def stop(self):
        if self.running:
            self.running = False
            self.report_loss()
            self.report_progress()

    def set_params(self,left_train_time,loss,progress):
        if left_train_time is not None:
            self.left_train_time = left_train_time
        if loss is not None:
            self.loss = loss
        if progress is not None:
            self.progress = progress