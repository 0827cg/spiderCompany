#!/usr/bin/python3 
"""
 Author: cg
 Date: 2020/11/16 17:07
"""


class Abstract:

    def init_def(self):
        """
        获取默认的配置数据
        :return:
        """
        raise NotImplementedError("待子类继承")

    @staticmethod
    def get_instance():
        """
        返回各自的实例
        :return:
        """
        raise NotImplementedError("待子类继承")
