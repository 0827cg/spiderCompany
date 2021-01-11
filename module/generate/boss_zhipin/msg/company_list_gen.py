#!/usr/bin/python3 
"""
 请求company列表的url, 获取到page内容

 采用requests解析内容失败，涉及到需要执行js，
 请求会跳转
 需要再次请求, 并执行js
 此情况下容易被封         ----2020-12-18 17:30

 采用selenium执行发现也会被封 -- 2020-12-29 11:19
 selenium只是单纯的打开页面就是, 有cookie, 难道是request 的header中referer这个字段.?

 在自己定义的selenium.py文件中增加了伪装代码__build_fake_options(),还是会被boss直聘认作为异常访问
 ---2020-12-30 16:42

 woc, 我刚测试发现,
 只要一直新开窗口访问boss直聘的url， 访问了8次, 就被封了(拿5，6个不同地址的url, 去新开窗口来访问, 重复到8次左右, 就会被封)
 奇葩
 如果真实这也
 那这boss直聘的程序员脑袋也太简单了吧,

 这也封的情况有两种
 1: 访问间隔, 频繁的访问中, 如果这几次的前后两次访问时间间隔 相似,
 2: 就是上面提到的, request的header中的referer这个字段为空, 连续几次都是空,

 url举例:
 ```
 https://www.zhipin.com/gongsi/2e4a5a34846d3da31nJ429g~.html
 https://www.zhipin.com/gongsi/019e0fa7c1e7761a1HZ-2Nu9.html
 https://www.zhipin.com/gongsi/f0dc27dca8d2b87d03R_09S0.html
 https://www.zhipin.com/gongsi/91c7f92e54d88c2603x_09-1.html
 https://www.zhipin.com/gongsi/2540c1868c94fb081XN439m_.html
 https://www.zhipin.com/gongsi/ed3d7f52374b575f33Fz2dm6.html
 ```
 --2020-12-30 16:50


 Author: cg
 Date: 2020/12/18 9:32
"""

from common.headers import headers
from utils import request_util
from utils import time_util
from utils import log_util
from module.generate.boss_zhipin.msg.boss_msg import BossZhiPinMsg
from module.selenium.msg.boss_company_list import BossCompanyList
from module.selenium.page_gen_mgr import PageGenMgr


class CompanyListGen(BossZhiPinMsg):

    def execute(self):
        base_url = request_util.get_base_url(self.url)
        if base_url is None:
            log_util.err_log.info("url unreasonable: {}".format(self.url))
            return
        # 采用浏览器解析，
        msg = BossCompanyList()
        msg.url = self.url
        PageGenMgr.put_execute(msg)

        # 取消使用requests来请求, 因为boss直聘 站点存在js解析, 准备采用selenium启动浏览器来解析页面
        # response = request_util.request(url=self.url, headers=headers)
        # if response is None:
        #     log_util.com_log.info("request not get data, url: {}".format(self.url))
        #     return
        # from module.generate.boss_zhipin.boss_mgr import BossZhiPinMgr
        # if not BossZhiPinMgr.has_base_url():
        #     BossZhiPinMgr.set_base_url(base_url)
        # log_util.com_log.info(response.text)
        # BossZhiPinMgr.analysis_list_page(response.text)
