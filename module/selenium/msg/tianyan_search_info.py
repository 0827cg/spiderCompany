#!/usr/bin/python3 
"""
 Author: cg
 Date: 2020/12/28 15:14
"""

from .page_msg import PageMsg
from ..selenium import SeleniumModule
from ..page_gen_mgr import PageGenMgr
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TianyanSearchInfo(PageMsg):

    # 搜索列表中得到的公司名字
    c_name = None

    # generate得到的类别
    category = None

    def execute(self):
        from module.research.tianyan_cha.tianyan_mgr import TianyanChaMgr
        SeleniumModule.get(self.url, self.name)
        element_present = EC.presence_of_element_located((By.CLASS_NAME, 'table -striped-col -breakall'))
        SeleniumModule.wait_element(element_present)
        PageGenMgr.set_busy(False)
        page_content = SeleniumModule.get_page_source(self.name)
        TianyanChaMgr.analysis_info(page_content, self.c_name, self.category, self.url)
