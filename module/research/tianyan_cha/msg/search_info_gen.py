#!/usr/bin/python3 
"""
 Author: cg
 Date: 2020/12/18 10:47
"""

from utils import request_util
from common.headers import headers
from module.research.tianyan_cha.msg.tianyan_msg import TianyanChaMsg
from utils import log_util
from module.selenium.msg.tianyan_search_info import TianyanSearchInfo
from module.selenium.page_gen_mgr import PageGenMgr


class SearchInfoGen(TianyanChaMsg):

    # 搜索列表中得到的公司名字
    c_name = None

    # generate得到的类别
    category = None

    def execute(self):
        msg = TianyanSearchInfo()
        msg.c_name = self.c_name
        msg.category = self.category
        msg.url = self.url
        PageGenMgr.put_execute(msg)
        # from module.research.tianyan_cha.tianyan_mgr import TianyanChaMgr
        # response = request_util.request(url=self.url, headers=headers, cookie_dict=self.cookie_dict)
        # if response is None:
        #     log_util.com_log.info("request not get data, url: {}".format(self.url))
        #     return
        # TianyanChaMgr.analysis_info(response.text, self.c_name, self.category, self.url)
