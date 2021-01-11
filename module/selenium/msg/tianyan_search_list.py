#!/usr/bin/python3 
"""
 Author: cg
 Date: 2020/12/25 16:47
"""

from .page_msg import PageMsg
from ..selenium import SeleniumModule
# from module.research.tianyan_cha.tianyan_mgr import TianyanChaMgr
from ..page_gen_mgr import PageGenMgr


class TianyanSearchList(PageMsg):

    # 所属类别(generate获取道的)
    category = None

    def execute(self):
        from module.research.tianyan_cha.tianyan_mgr import TianyanChaMgr
        SeleniumModule.get(self.url, self.name)
        PageGenMgr.set_busy(False)
        page_content = SeleniumModule.get_page_source(self.name)
        TianyanChaMgr.analysis_search_list(page_content, self.category)
