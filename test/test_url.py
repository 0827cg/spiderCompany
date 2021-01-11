#!/usr/bin/python3 
"""
 Author: cg
 Date: 2020/12/31 9:51
"""

from utils import request_util


def test_url(value):
    url = "https://www.tianyancha.com/search"
    dict_params = {
        "key": value
    }
    print("type params: {}".format(type(dict_params)))
    url = request_util.op_single_rec(url, dict_params, False)
    print(url)

test_url("测试")
