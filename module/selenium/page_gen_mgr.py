#!/usr/bin/python3 
"""
 Author: cg
 Date: 2020/12/25 15:58
"""
import logging
from queue import Queue
from utils import log_util
from module.config_mgr import ConfigMgr
from .msg.page_msg import PageMsg
from .selenium import SeleniumModule


class PageGenMgr:

    # 大小无限制的队列, 存放对象(PageMsg子类对象)
    __queue = Queue(maxsize=0)

    # 是否忙碌, 需等待上一条执行完成
    __busy = False

    @classmethod
    def start(cls, scheduler):
        # 1秒取一次来执行
        cls.init()
        scheduler.add_job(cls.run, 'interval', max_instances=10, seconds=1)
        log_util.com_log.info("PageGenMgr started...")

    @classmethod
    def stop(cls):
        log_util.com_log.info("stop PageGenMgr")
        SeleniumModule.quit()

    @classmethod
    def run(cls):
        if cls.__busy:
            return
        if cls.__queue.empty():
            return
        msg = cls.__queue.get_nowait()
        if msg is None:
            return
        try:
            cls.__busy = True
            msg.execute()
        except BaseException as error:
            log_util.err_log.error("execute func error: {}, msg: {}".format(error, msg.__dict__))
            # 上一个消息错误后, 设置状态空闲
            cls.__busy = False
        finally:
            log_util.com_log.info("check")
            SeleniumModule.check()

    @classmethod
    def test_run(cls):
        log_util.com_log.info("test run")

    @classmethod
    def init(cls):
        # 启动浏览器
        headless = ConfigMgr.get_config("base").headless
        driver_path = ConfigMgr.get_config("base").chrome_driver_path
        SeleniumModule.init(headless, driver_path=driver_path)

    @classmethod
    def put_execute(cls, msg):
        if not isinstance(msg, PageMsg):
            return
        cls.__queue.put(msg)

    @classmethod
    def set_busy(cls, busy):
        cls.__busy = busy
