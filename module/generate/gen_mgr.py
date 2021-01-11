#!/usr/bin/python3 
"""
 初衷用来管理所有的generate, 即得到公司名字的, 如从boss直聘招聘网得到的公司名字
 Author: cg
 Date: 2020/12/18 11:14
"""

from module.generate.boss_zhipin.boss_mgr import BossZhiPinMgr
from utils import log_util


class GenMgr:

    @classmethod
    def start(cls, scheduler):
        # 目前仅有boss直聘在启动
        BossZhiPinMgr.start(scheduler)
        log_util.com_log.info("GenMgr started...")

    @classmethod
    def stop(cls):
        BossZhiPinMgr.stop()
        log_util.com_log.info("stop GenMgr")

    # @classmethod
    # def handle_list_page(cls, url, re_build=True):
    #     if re_build:
    #         url = BossZhiPinMgr.get_base_url() + url
    #     list_gen = CompanyListGen()
    #     list_gen.url = url
    #     BossZhiPinMgr.put_execute(list_gen)
    #
    # @classmethod
    # def handle_info_page(cls, url, category, re_build=True):
    #     if re_build:
    #         url = BossZhiPinMgr.get_base_url() + url
    #     info_gen = CompanyInfoGen()
    #     info_gen.category = category
    #     info_gen.url = url
    #     BossZhiPinMgr.put_execute(info_gen)