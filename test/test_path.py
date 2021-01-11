#!/usr/bin/python3 
"""
 Author: cg
 Date: 2020/12/18 15:35
"""

import os

dir_path = "D:\\work\\python\\pycharm\\200506\\spiderCompany\\res_page"

file_name = "t.txt"

dir_name = "out"

f_path = os.path.join(dir_path, file_name)
save_path = os.path.join(dir_path, dir_name)
print(f_path)
print(save_path)