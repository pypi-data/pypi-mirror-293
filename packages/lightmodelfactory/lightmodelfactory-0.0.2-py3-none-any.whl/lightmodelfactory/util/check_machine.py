#!/usr/bin/env python
# coding:utf-8
""" 
@author: nivic ybyang7
@license: Apache Licence 
@file: check_machine
@time: 2024/08/15
@contact: ybyang7@iflytek.com
@site:  
@software: PyCharm 

# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛ 
"""

#  Copyright (c) 2022. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.

import os
import subprocess
from typing import Literal


def is_npu():
    return check_tool("npu-smi")


def check_tool(tool):
    cmd = [f"which {tool}"]
    ret = subprocess.call(cmd, shell=True)
    if ret != 0:
        return False
    return True


def get_file_format(fi) -> [ Literal[True, False],Literal["json", "jsonl", "csv"]]:
    """
    返回
    """
    if not os.path.exists(fi):
        return False, ""
    if fi.endswith(".json"):
        fmt = "json"
    elif fi.endswith(".jsonl"):
        fmt = "jsonl"
    elif fi.endswith(".csv"):
        fmt = 'csv'
    return True, fmt

