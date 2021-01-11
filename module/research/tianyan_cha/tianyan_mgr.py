#!/usr/bin/python3 
"""
 Author: cg
 Date: 2020/12/18 10:27
"""
import logging
from queue import Queue
from bs4 import BeautifulSoup
from utils import com_util
from utils import log_util
from utils import string_util
from utils import time_util
from utils import request_util
from module.config_mgr import ConfigMgr
from module.research.tianyan_cha.msg.tianyan_msg import TianyanChaMsg
from module.research.tianyan_cha.msg.search_list_gen import SearchListGen
from module.research.tianyan_cha.msg.search_info_gen import SearchInfoGen
from module.research.tianyan_cha.tianyan_result import TianyanResult
from module.selenium.msg.site_add_cookie import SiteAddCookies
from module.result.result_mgr import ResultMgr
from module.selenium.page_gen_mgr import PageGenMgr


class TianyanChaMgr:
    __cookie_dict = None

    __base_url = None

    # 搜索用的url
    __search_url = None

    # 大小无限制的队列, 存放对象(TianyanChaMsg子类对象), 先进先出
    __queue = Queue(maxsize=0)

    @classmethod
    def start(cls, scheduler):
        # 5秒取一次来执行 run方法
        cls.init()
        scheduler.add_job(cls.run, 'interval', seconds=20)
        log_util.com_log.info("TianyanChaMgr started...")

    @classmethod
    def stop(cls):
        log_util.com_log.info("stop TianyanChaMgr")

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
        # 初始化第一次请求
        search_url = ConfigMgr.get_config("base").tianyanCha
        if string_util.is_empty(search_url):
            log_util.err_log.error("search url is empty")
            return
        cls.__search_url = search_url
        cls.__base_url = request_util.get_base_url(search_url)

        # 让浏览器先拥有天眼查账户cookie
        msg = SiteAddCookies()
        msg.key = "tianyan"
        msg.path = ConfigMgr.get_config("base").tianyanCha_cookie
        msg.url = cls.__base_url
        PageGenMgr.put_execute(msg)

    @classmethod
    def put_execute(cls, msg):
        if not isinstance(msg, TianyanChaMsg):
            return
        cls.__queue.put(msg)

    @classmethod
    def set_base_url(cls, url):
        cls.__base_uri = url

    @classmethod
    def has_base_url(cls):
        return cls.__base_url is None

    @classmethod
    def analysis_search_list(cls, page, category):
        soup = BeautifulSoup(page, "html.parser")
        container_tags = soup.find("div", class_="result-list sv-search-container")
        item_tags = container_tags.find_all("div", class_="search-item sv-search-company")
        if len(item_tags) <= 0:
            log_util.com_log.info("not company found in search page")
            return
        result_tag = item_tags[0]
        company_name_tag = result_tag.find("div", class_="info")
        company_name = company_name_tag.get_text()
        if company_name is None:
            log_util.com_log.info("company name not found in search page")
            return
        href_tag = result_tag.find("a", class_="name")
        href_url = href_tag.get("href")
        if string_util.is_empty(href_url):
            log_util.com_log.info("company info url not found in search page")
            return
        # print(href_url)

        # 将搜索列表中的公司名字传入, 打开解析详情页
        cls.handle_info_gen(href_url, company_name, category)

    @classmethod
    def analysis_info(cls, page, c_name, category, url):
        result = TianyanResult()
        result.name = c_name
        result.category = category
        soup = BeautifulSoup(page, "html.parser")
        contact_tag = soup.find("div", class_="in-block sup-ie-company-header-child-1")
        phone_tag = contact_tag.find("span", class_="label")
        phone_span_tag = phone_tag.next_sibling
        phone_num = phone_span_tag.get_text()
        if string_util.is_empty(phone_num):
            log_util.com_log.info("company {} phone not found".format(c_name))
        result.tel = phone_num

        # 最近更新
        update_tag = soup.find("span", class_="updatetimeComBox")
        result.last_update = update_tag.get_text()

        info_tag = soup.find("table", class_="table -striped-col -breakall")
        name_tag = info_tag.find("div", class_="name")
        name_a_tag = name_tag.find("a", class_="link-click")

        # 法定代表人
        result.legal = name_a_tag.get_text()

        tr_tags = info_tag.find_all("tr")

        # 成立日期
        result.establish_date = cls.__get_contents(tr_tags, 1, 1)
        # 行业
        result.sector = cls.__get_contents(tr_tags, 6, 3)
        # 规模
        result.scope = cls.__get_contents(tr_tags, 6, 5)

        # 地址
        result.address = cls.__get_contents(tr_tags, 9, 1)

        # 经营范围
        result.business_scope = cls.__get_contents(tr_tags, 10, 1)
        result.gain_mills = time_util.getcurrent_ts_millis()
        result.url = url

        # 修改resultMgr处理
        ResultMgr.put(result)

    @staticmethod
    def __get_contents(tr_tags, tr_index, content_index):
        try:
            if len(tr_tags) <= tr_index:
                return None
            contents = tr_tags[tr_index]
            if len(contents) <= content_index:
                return None
            return contents[content_index].get_text()
        except BaseException as error:
            log_util.err_log.error(error)
            return None

    @classmethod
    def handle_search(cls, name, category):
        list_gen = SearchListGen()
        list_gen.value = name
        list_gen.category = category
        list_gen.url = cls.__search_url
        list_gen.cookie_dict = cls.__cookie_dict
        cls.put_execute(list_gen)

    @classmethod
    def handle_info_gen(cls, url, c_name, category):
        info_gen = SearchInfoGen()
        info_gen.c_name = c_name
        info_gen.category = category
        info_gen.url = url
        info_gen.cookie_dict = cls.__cookie_dict
        cls.put_execute(info_gen)
