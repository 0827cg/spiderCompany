#!/usr/bin/python3 
"""
 Author: cg
 Date: 2020/12/18 9:49
"""

from module.generate.boss_zhipin.msg.boss_msg import BossZhiPinMsg
from module.selenium.msg.boss_company_info import BossCompanyInfo
from module.selenium.page_gen_mgr import PageGenMgr
from utils import time_util
from utils import request_util
from common.headers import headers
from utils import log_util


class CompanyInfoGen(BossZhiPinMsg):
    # 类别
    category = None

    # headers referer url
    referer = None

    def execute(self):

        msg = BossCompanyInfo()
        msg.url = self.url
        # msg.name = str(time_util.getcurrent_ts_millis())
        msg.referer = self.referer
        msg.category = self.category
        PageGenMgr.put_execute(msg)

        # from module.generate.boss_zhipin.boss_mgr import BossZhiPinMgr
        # response = request_util.request(url=self.url, headers=headers)
        # if response is None:
        #     log_util.com_log.info("request not get data, url: {}".format(self.url))
        #     return
        # BossZhiPinMgr.analysis_info_page(response.text, self.category)
