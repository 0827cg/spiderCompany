#!/usr/bin/python3 
"""
 Author: cg
 Date: 2020/12/17 11:44
"""
import os.path



# 当前文件的绝对路径来获得文件所在目录
current_path = os.path.abspath(__file__)
str_path = "D:\\work\\python\\pycharm\\200506\\spiderCompany\\conf\\Base.json"
dir_path = os.path.dirname(str_path)
print(dir_path)