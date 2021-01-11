#!/usr/bin/python3 
"""
 Author: cg
 Date: 2020/12/28 14:02
"""

from .page_msg import PageMsg
from ..selenium import SeleniumModule
from ..page_gen_mgr import PageGenMgr


class SiteAddCookies(PageMsg):

    # 站点标识
    key = None

    # 存放cookie的txt文件路径
    path = None

    def execute(self):
        SeleniumModule.site_add_cookies(self.key, self.url, name=self.name, cookie_path=self.path)
        PageGenMgr.set_busy(False)
