#!/usr/bin/python3 
"""
 Author: cg
 Date: 2020/12/18 10:26
"""


class TianyanChaMsg:
    # 请求的url
    url = None

    # cookie
    cookie_dict = None

    def execute(self):
        raise NotImplementedError("待子类继承")
