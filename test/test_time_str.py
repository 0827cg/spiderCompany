#!/usr/bin/python3 
"""
 Author: cg
 Date: 2020/12/25 16:32
"""

from utils import time_util

mills = time_util.getcurrent_ts_millis()
print(type(mills))
print(mills)
str_mills = str(mills)
print(type(str_mills))
print(str_mills)
