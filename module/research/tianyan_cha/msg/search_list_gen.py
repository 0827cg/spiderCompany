#!/usr/bin/python3 
"""
 Author: cg
 Date: 2020/12/18 10:44
"""

from utils import request_util
from common.headers import headers
from module.research.tianyan_cha.msg.tianyan_msg import TianyanChaMsg
from utils import log_util
from utils import time_util
from module.selenium.msg.tianyan_search_list import TianyanSearchList
from module.selenium.page_gen_mgr import PageGenMgr


class SearchListGen(TianyanChaMsg):
    # 搜索的内容
    value = None

    # 所属类别(generate获取道的)
    category = None

    def execute(self):
        # from module.research.tianyan_cha.tianyan_mgr import TianyanChaMgr
        dict_params = {
            "key": self.value
        }
        url = request_util.op_single_rec(self.url, dict_params, False)
        msg = TianyanSearchList()
        msg.url = url
        # msg.name = str(time_util.getcurrent_ts_millis())
        msg.category = self.category
        PageGenMgr.put_execute(msg)

        # response = request_util.request(url=url, headers=headers, cookie_dict=self.cookie_dict)
        # if response is None:
        #     log_util.com_log.info("request not get data, url: {}".format(self.url))
        #     return
        # TianyanChaMgr.analysis_search_list(response.text, self.category)
