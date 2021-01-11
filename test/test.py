#!/usr/bin/python3 
"""
 Author: cg
 Date: 2020/12/16 14:50
"""
from module.config_mgr import ConfigMgr


def test():

    # ConfigMgr
    print("test")


def test_char():
    value = "贸易/进出口"
    value = value.replace('/', '-')
    print(value)

test_char()


