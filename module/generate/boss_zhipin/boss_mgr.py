#!/usr/bin/python3 
"""
 Author: cg
 Date: 2020/12/17 17:52
"""

from queue import Queue
from bs4 import BeautifulSoup
from utils import log_util
from utils import string_util
from utils import request_util
from module.config_mgr import ConfigMgr
from module.generate.boss_zhipin.msg.boss_msg import BossZhiPinMsg
from module.generate.boss_zhipin.msg.company_list_gen import CompanyListGen
from module.generate.boss_zhipin.msg.company_info_gen import CompanyInfoGen
from module.selenium.msg.site_add_cookie import SiteAddCookies
from module.generate.gen_msg import GenMsg
from module.research.research_mgr import ResearchMgr
from module.selenium.page_gen_mgr import PageGenMgr


class BossZhiPinMgr:
    __cookie_dict = None

    # 基本url, 协议+域名
    __base_url = None

    # 大小无限制的队列, 存放对象(BossZhiPinMsg子类对象)
    __queue = Queue(maxsize=0)

    @classmethod
    def start(cls, scheduler):
        # 4秒取一次来执行
        scheduler.add_job(cls.run, 'interval', seconds=60)
        log_util.com_log.info("BossZhiPinMgr started...")
        cls.init()

    @classmethod
    def stop(cls):
        log_util.com_log.info("stop BossZhiPinMgr")

    @classmethod
    def run(cls):
        if cls.__queue.empty():
            return
        msg = cls.__queue.get_nowait()
        if msg is None:
            return
        try:
            msg.execute()
        except BaseException as error:
            log_util.err_log.error("execute func error: {}".format(error))

    @classmethod
    def init(cls):
        boss_url = ConfigMgr.get_config("base").bossZhiPin
        if len(boss_url) <= 0:
            log_util.err_log.error("boss zhipin url is empty, must configuration")
            return
        cls.__base_url = request_util.get_base_url(boss_url[0])
        # 让浏览器先拥有boss直聘上面的cookie
        msg = SiteAddCookies()
        msg.key = "boss"
        msg.path = ConfigMgr.get_config("base").bossZhiPin_cookie
        msg.url = cls.__base_url
        PageGenMgr.put_execute(msg)

        # 初始化第一次请求
        for url in boss_url:
            cls.handle_list_page(url, False)

    @classmethod
    def put_execute(cls, msg):
        if not isinstance(msg, BossZhiPinMsg):
            return
        cls.__queue.put(msg)

    @classmethod
    def set_base_url(cls, url):
        cls.__base_uri = url

    @classmethod
    def get_base_url(cls):
        return cls.__base_url

    @classmethod
    def has_base_url(cls):
        return cls.__base_url is None

    @classmethod
    def analysis_list_page(cls, url, page):
        """
        boss直聘公司列表页面解析
        :param url: 页面的url(用来设置下一级页面的referer)
        :param page: 页面源代码
        :return: None
        """
        soup = BeautifulSoup(page, "html.parser")

        # 类别
        selected_tag = soup.find_all("span", class_="dropdown-select selected")
        category = str()
        for item in selected_tag:
            if item is None:
                continue
            item = item.get_text().replace('/', '+')
            category += item

        # item
        tag = soup.find("div", class_="company-tab-box company-list")
        item_tags = tag.find_all("div", class_="sub-li")
        if item_tags is None:
            log_util.com_log.info("not found company item info in page list")
            return
        for item in item_tags:
            a_tag = item.find("a", class_="company-info")
            item_href = a_tag.get("href")
            if item_href is None:
                log_util.com_log.info("item href not found in page list")
                continue
            cls.handle_info_page(url, item_href, category)

        next_tag = tag.find("a", class_="next")
        if next_tag is None:
            log_util.com_log.info("not found next a tag in page list")
            return
        next_href = next_tag.get("href")
        cls.handle_list_page(next_href)

    @classmethod
    def analysis_info_page(cls, page, category):
        soup = BeautifulSoup(page, "html.parser")
        info_tag = soup.find("div", class_="job-sec company-business")
        name_tag = info_tag.find("h4")
        if name_tag is None:
            log_util.com_log.info("not found company info in page")
            return
        company_name = name_tag.contents[1]
        gen_msg = GenMsg()
        gen_msg.gen_name = cls.__name__
        gen_msg.name = company_name
        gen_msg.category = category
        # 丢给research模块进一步处理
        ResearchMgr.put(gen_msg)

    @classmethod
    def handle_list_page(cls, url, re_build=True):
        if re_build:
            url = cls.__base_url + url
        list_gen = CompanyListGen()
        list_gen.url = url
        cls.put_execute(list_gen)

    @classmethod
    def handle_info_page(cls, referer_url, url, category, re_build=True):
        """
        构建请求公司信息的页面
        :param referer_url: referer
        :param url: 公司信息页面uri
        :param category: 标签
        :param re_build: 是否重新组合url, 默认true
        :return: None
        """
        if re_build:
            url = cls.__base_url + url
        info_gen = CompanyInfoGen()
        info_gen.category = category
        info_gen.referer = referer_url
        info_gen.url = url
        cls.put_execute(info_gen)
