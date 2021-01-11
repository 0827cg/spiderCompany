#!/usr/bin/python3 
"""
 Author: cg
 Date: 2020/12/16 13:55
"""

import os
from common import const
from common.schema.config.abstract import Abstract


class Base(Abstract):
    # 同一个网站请求间隔时间, 毫秒
    gapMillsSameSite = None

    # 存放输出目录
    outDirPath = None

    # boss直接聘 页面url, 集合
    bossZhiPin = list()

    # boss直聘 cookie txt文件路径
    bossZhiPin_cookie = None

    # 天眼查 的搜索url
    tianyanCha = None

    # 天眼查用的cookie, txt文件路径
    tianyanCha_cookie = None

    # 是否启用无头
    headless = None

    # chrome驱动路径
    chrome_driver_path = None

    def init_def(self):
        cur_path = os.getcwd()
        self.gapMillsSameSite = const.sameSiteReqGapValue
        self.outDirPath = os.path.join(cur_path, const.outDirValue)
        self.bossZhiPin = const.bossZhiPinValue
        self.bossZhiPin_cookie = const.bossZhiPinCookieValue
        self.tianyanCha = const.tianyanChaValue
        self.tianyanCha_cookie = const.tianyanChaCookieValue
        self.headless = const.headlessValue
        self.chrome_driver_path = const.chrome_driver_value

    @staticmethod
    def get_instance():
        return Base()
