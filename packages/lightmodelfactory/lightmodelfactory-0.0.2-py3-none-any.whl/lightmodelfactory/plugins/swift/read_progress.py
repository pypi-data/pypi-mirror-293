import time
import threading
import os
import json
from lightmodelfactory.util.logger import logger
import re

'''
{"loss": 1.85694408, "acc": 0.59182997, "grad_norm": 1.7578125, "learning_rate": 8e-08, 
"memory(GiB)": 15.83, "train_speed(iter/s)": 0.218112, "epoch": 0.96969697, 
"steps[global_step/max_steps]": "60/61", "percentage": "98.36%", 
"elapsed_time": "4m 34s", "remaining_time": "4s"}
'''
def time_str_to_seconds(time_str):
    minutes = 0
    seconds = 0
    
    match_minutes = re.search(r'(\d+)m', time_str)
    if match_minutes:
        minutes = int(match_minutes.group(1))
    
    match_seconds = re.search(r'(\d+)s', time_str)
    if match_seconds:
        seconds = int(match_seconds.group(1))
    
    total_seconds = minutes * 60 + seconds
    return total_seconds

#/home/swift/output_cn_llama3/llama3-8b-instruct/v0-20240715-143139/logging.jsonl
class FileMonitorThread(threading.Thread):
    def __init__(self, output_dir, train_progress_cb):
        super().__init__()
        self.output_dir = output_dir
        self.file_path = None
        self.last_position = 0
        self.running = True
        self.train_progress_cb = train_progress_cb

    def run(self):
        target_filename = "logging.jsonl"
        noFound = True
        while noFound and self.running:
            for dirpath, _, filenames in os.walk(self.output_dir):
                if target_filename in filenames:
                    self.file_path = os.path.join(dirpath, target_filename)
                    logger.info(f"{target_filename} 文件存在于 {self.file_path} 中。")
                    noFound = False
                    break
            time.sleep(1)

        self.poll_file()

    def poll_file(self):
        reading = True
        while self.running and reading:
            if os.path.isfile(self.file_path):
                with open(self.file_path, 'r') as f:
                    f.seek(self.last_position)
                    while True:
                        line = f.readline()
                        if not line:
                            break
                        data = json.loads(line)

                        loss = data.get('loss', None)
                        percentage_value  = data.get('percentage', None)
                        percentage = None
                        if percentage_value is not None:
                            percentage = float(percentage_value.strip("%"))  
                        remaining_time_str = data.get('remaining_time', None)
                        left_train_time = 0

                        if remaining_time_str is not None:
                            left_train_time = time_str_to_seconds(remaining_time_str)

                        self.train_progress_cb(left_train_time, percentage, loss)
                        
                        if percentage is not None and (abs(percentage - 100) < 1e-7):
                            reading = False
                            break

                    self.last_position = f.tell()

            time.sleep(1)

    def stop(self):
        self.running = False
