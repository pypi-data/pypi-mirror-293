import time
import threading
import os
import json
from lightmodelfactory.util.logger import logger

'''
{"current_steps": 70, "total_steps": 1011, "loss": 64.8195, "learning_rate": 5e-06, "epoch": 0.2074074074074074, "percentage": 6.92, "elapsed_time": "0:02:51", "remaining_time": "0:38:28"}
'''
def time_str_to_seconds(time_str):
    import re
    pattern = r'(?:(\d+)\s*days?,\s*)?(\d+):(\d+):(\d+)'
    match = re.match(pattern, time_str)
    if match:
        days = int(match.group(1)) if match.group(1) else 0
        hours = int(match.group(2))
        minutes = int(match.group(3))
        seconds = int(match.group(4))
        total_seconds = days * 86400 + hours * 3600 + minutes * 60 + seconds
        return total_seconds
    else:
        raise ValueError("Invalid time format")

class FileMonitorThread(threading.Thread):
    def __init__(self, output_dir, train_progress_cb):
        super().__init__()
        self.output_dir = output_dir
        self.file_path = os.path.join(output_dir, 'trainer_log.jsonl')
        self.last_position = 0
        self.running = True
        self.train_progress_cb = train_progress_cb

    def run(self):
        while not os.path.exists(self.output_dir):
            time.sleep(1)
            if not self.running:
                return
        
        while not os.path.isfile(self.file_path):
            time.sleep(1)
            if not self.running:
                return

        self.poll_file()

    def poll_file(self):
        while self.running:
            if os.path.isfile(self.file_path):
                with open(self.file_path, 'r') as f:
                    f.seek(self.last_position)
                    while True:
                        line = f.readline()
                        if not line:
                            break
                        data = json.loads(line)

                        loss = data.get('loss', None)
                        percentage = data.get('percentage', None)
                        remaining_time_str = data.get('remaining_time', None)
                        left_train_time = 0

                        if remaining_time_str is not None:
                            left_train_time = time_str_to_seconds(remaining_time_str)

                        self.train_progress_cb(left_train_time, percentage, loss)

                    self.last_position = f.tell()

            time.sleep(1)

    def stop(self):
        self.running = False
