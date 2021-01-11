#!/usr/bin/python3 
"""

 用来获取网页源代码

 针对需要进行js执行的页面

 使用火狐浏览器, 需要指定火狐驱动地址

 单例存在

 # seleniumwire==1.0.6

 Author: cg
 Date: 2020/12/25 9:39
"""
# from selenium import webdriver
from seleniumwire import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from module.config_mgr import ConfigMgr
from utils import log_util
from utils import file_util
from utils import com_util
from utils import time_util


class SeleniumModule:
    __browser = None

    # chrome驱动存放地址
    __chrome_driver_path = "D:\\work\\python\\pycharm\\200506\\spiderCompany\\lib\\chromedriver_win32\\chromedriver.exe"

    # key: name, value: windows_handlers[x]地址
    __windows_dict = dict()

    # 已经操作完成的标签窗口
    __windows_complete_dict = dict()

    # 是否是第一次请求
    __first_get = False

    # 添加了cookie的网站信息, key: name, value: boolean
    __site_add_cookie = dict()

    # 窗口的最大个数
    __windows_num_max = 6

    @classmethod
    def init(cls, headless=True, driver_path=None, page_time_out=15):
        """
        浏览器初始化
        :param headless: 是否采用无头浏览器(无界面)
        :param driver_path: chrome驱动路径
        :param page_time_out: 单个页面请求的超时时间, 秒, 默认15秒
        :return:
        """
        options = Options()
        cls.__build_fake_options(options)
        options.headless = headless
        if driver_path is None:
            driver_path = cls.__chrome_driver_path
        cls.__browser = webdriver.Chrome(options=options, executable_path=driver_path)
        # 启动好, 并存在一个空白标签, 等待执行get, ,webDriver基类中已经调用了start_client(), 这里不需要另外执行
        # cls.__browser.start_client()
        cls.__browser.set_page_load_timeout(page_time_out)
        log_util.com_log.info("browser started...")

    @classmethod
    def quit(cls):
        cls.__browser.quit()
        log_util.com_log.info("stop browser")

    @classmethod
    def check(cls):
        """
        长度检测
        :return:
        """

        if len(cls.__windows_dict) < cls.__windows_num_max:
            return

        for k, _ in cls.__windows_complete_dict.items():
            if k not in cls.__windows_dict:
                continue
            log_util.com_log.info("k: {}".format(k))
            cls.close_tab(k)
            del cls.__windows_dict[k]

    @classmethod
    def get(cls, url, name, new_tab=True):
        """
        请求一个url,
        :param url: url
        :param name: string唯一标识
        :param new_tab: 默认打开新的标签
        :return: None
        """
        if not isinstance(url, str) or not isinstance(name, str):
            log_util.err_log.error("url or name type unreasonable")
            return
        if cls.__browser is None:
            log_util.err_log.error("browser not init")
            return

        suc = False
        if cls.__first_get is False:
            # 第一次
            suc = cls.__get(url)
        else:
            if new_tab:
                cls.new_tab()
            suc = cls.__get(url)
        # elif new_tab:
        #     cls.new_tab()
        #     suc = cls.__get(url)
        if suc:
            cls.__windows_dict[name] = cls.__browser.current_window_handle
            if cls.__first_get is False:
                cls.__first_get = True
        else:
            # 请求超时将关闭该标签页
            if cls.__first_get is False:
                cls.new_tab(False)
            cls.close_tab()
            cls.switch_window_index()

    @classmethod
    def __get(cls, url):
        b_mill = time_util.getcurrent_ts_millis()
        try:
            cls.__browser.get(url)
        except TimeoutException:
            log_util.err_log.error("url: {} request time out".format(url))
            return False

        e_mill = time_util.getcurrent_ts_millis()
        cost = (e_mill - b_mill) / 1000
        log_util.com_log.info("url: {} request success, cost: {} seconds".format(url, cost))
        return True

    @classmethod
    def refresh(cls, name=None):
        """
        标签窗口刷新
        :param name: 唯一标识
        :return: boolean true: 成功刷新
        """
        if name is None:
            cls.__browser.refresh()
            return True
        switch = cls.switch_window(name)
        if switch:
            cls.__browser.refresh()
            return True
        return False

    @classmethod
    def get_page_source(cls, name=None):
        """
        根据唯一标识, 获得页面源码
        :param name: 唯一标识
        :return:
        """
        if name is None:
            return cls.__browser.page_source
        res = cls.switch_window(name)
        if res:
            cls.mark_complete(name)
            return cls.__browser.page_source
        return None

    @classmethod
    def switch_window(cls, name):
        """
        根据唯一标识来切换标签窗口
        :param name: 唯一标识 str
        :return: boolean true: 成功
        """
        if name not in cls.__windows_dict:
            return False
        windows_handle = cls.__windows_dict[name]
        if windows_handle is None:
            return False
        cls.__browser.switch_to.window(windows_handle)
        return True

    @classmethod
    def switch_window_index(cls, index=None):
        """
        根据下标来切换标签窗口
        :param index: None: 最后一个
        :return:
        """
        if index is None:
            index = cls.get_now_index_max()
        windows_handle = cls.get_windows_handle(index)
        if windows_handle is None:
            return None
        cls.__browser.switch_to.window(windows_handle)

    @classmethod
    def new_tab(cls, switch=True):
        """
        打开新的标签窗口
        :param switch: browser是否切换过去, 默认切换
        :return: None
        """
        old_index = cls.get_now_index_max()
        cls.__browser.execute_script("window.open('');")
        windows_handle = cls.get_windows_handle(old_index + 1)
        # cls.__windows_dict[name] = windows_handle
        if not switch:
            return
        cls.__browser.switch_to.window(windows_handle)

    @classmethod
    def close_tab(cls, name=None):
        """
        根据名字来关闭标签窗口
        :param name: None: 关闭当前
        :return:
        """
        old_index = cls.get_now_index_max()
        if name is not None:
            res = cls.switch_window(name)
            if not res:
                return False
        cls.__browser.close()
        cls.switch_window_index(old_index - 1)
        return True

    @classmethod
    def get_now_index_max(cls):
        """
        cls.__browser在init初始化后, 本身就会创建一个windows_handle存放在window_handles中
        所以初始化后, windows_handles的大小就为1
        :return:
        """
        return len(cls.__browser.window_handles) - 1

    @classmethod
    def get_windows_handle(cls, index=None):
        """
        根据下标来获取window_handle
        :param index:
        :return:
        """
        if index is None:
            now_index = cls.get_now_index_max()
            if now_index < 0:
                return None
            return cls.__browser.window_handles[now_index]
        if not isinstance(index, int):
            return None
        return cls.__browser.window_handles[index]

    @classmethod
    def get_browser(cls):
        return cls.__browser

    @classmethod
    def mark_complete(cls, name):
        """
        标志完成
        :param name: 标签名字
        :return:
        """
        if name not in cls.__windows_dict:
            return
        if name in cls.__windows_complete_dict:
            return
        cls.__windows_complete_dict[name] = True
        log_util.com_log.info("complete_dict: {}".format(cls.__windows_complete_dict))

    @classmethod
    def add_cookie(cls, key, cookie):
        cls.__browser.add_cookie(cookie)
        cls.__site_add_cookie[key] = True

    @classmethod
    def add_cookies(cls, key, cookies):
        for item in cookies:
            cls.add_cookie(key, item)

    @classmethod
    def delete_all_cookies(cls):
        cls.__browser.delete_all_cookies()

    @classmethod
    def has_add_cookie(cls, key):
        """
        是否过该标识网站的cookie
        :param key: 网站标识
        :return: boolean True: 添加过了
        """
        if key not in cls.__site_add_cookie:
            return False
        return cls.__site_add_cookie[key]

    @classmethod
    def site_add_cookies(cls, key, url, name, cookie_path):
        """
        为站点添加cookie, 新开一个标签窗口来添加cookie, 往后会自己记录
        :param key: 站点标识
        :param url: 站点url
        :param name: 标签窗口标识
        :param cookie_path: 存放的cookie .txt路径
        :return: None
        """
        if cls.has_add_cookie(key):
            return
        log_util.com_log.info("try add cookie for site: {}, key: {}".format(url, key))
        str_cookie = file_util.read_file(cookie_path)
        if str_cookie is None:
            return
        list_cookie = com_util.parse_to_dict(str_cookie)
        cls.get(url, name)
        cls.delete_all_cookies()
        cls.add_cookies(key, list_cookie)
        cls.refresh()

    @classmethod
    def __build_fake_options(cls, options):
        options.add_experimental_option('useAutomationExtension', False)
        # 为实现window.navigator.webdriver为null, 第二个有用对我
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_argument("--disable-blink-features=AutomationControlled")

        options.add_argument("--disable-blink-features")
        options.add_argument("--disable-blink-features=AutomationControlled")

    @classmethod
    def wait(cls):
        """
        测试
        :return:
        """
        cls.__browser.implicitly_wait(10)

    @classmethod
    def wait_element(cls, element_present):
        WebDriverWait(cls.__browser, 10).until(element_present)


    @classmethod
    def add_headers(cls, k, v):
        cls.__browser.header_overrides = {
            k: v
        }

    @classmethod
    def add_headers_referer(cls, value):
        cls.add_headers("Referer", value)
