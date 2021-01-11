#!/usr/bin/python3 
"""
 Author: cg
 Date: 2020/12/25 16:02
"""
from utils import time_util


class PageMsg:

    url = None

    # 标签窗口名字, 默认为当前时间戳
    name = str(time_util.getcurrent_ts_millis())

    def execute(self):
        raise NotImplementedError("待子类继承")
