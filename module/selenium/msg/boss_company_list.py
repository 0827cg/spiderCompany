#!/usr/bin/python3 
"""
 Author: cg
 Date: 2020/12/25 16:18
"""

from .page_msg import PageMsg
from ..selenium import SeleniumModule
from ..page_gen_mgr import PageGenMgr


class BossCompanyList(PageMsg):

    def execute(self):
        """
        被取到后, 直接执行请求, 然后设置不忙(允许浏览器再次期间执行别的请求), 然后就进行内容解析
        丢到BossZhiPinMgr这个mgr里面去解析, 这一步就不走队列了, 直接解析
        :return:
        """
        from module.generate.boss_zhipin.boss_mgr import BossZhiPinMgr
        SeleniumModule.get(self.url, self.name)
        PageGenMgr.set_busy(False)
        page_content = SeleniumModule.get_page_source(self.name)
        BossZhiPinMgr.analysis_list_page(self.url, page_content)
