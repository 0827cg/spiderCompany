#!/usr/bin/python3 
"""
 Author: cg
 Date: 2020/12/25 16:40
"""

from .page_msg import PageMsg
from ..selenium import SeleniumModule
# from module.generate.boss_zhipin.boss_mgr import BossZhiPinMgr
from ..page_gen_mgr import PageGenMgr


class BossCompanyInfo(PageMsg):
    # 类别
    category = None

    # headers referer url
    referer = None

    def execute(self):
        from module.generate.boss_zhipin.boss_mgr import BossZhiPinMgr
        SeleniumModule.add_headers_referer(self.referer)
        SeleniumModule.get(self.url, self.name)
        SeleniumModule.wait()
        PageGenMgr.set_busy(False)
        page_content = SeleniumModule.get_page_source(self.name)
        BossZhiPinMgr.analysis_info_page(page_content, self.category)
