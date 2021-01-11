#!/usr/bin/python3 
"""
 Author: cg
 Date: 2020/12/16 14:21
"""

import sys
import signal
import logging
import logging.config
from utils import log_cfg
from utils import log_util
from module.config_mgr import ConfigMgr
from module.generate.gen_mgr import GenMgr
from module.research.research_mgr import ResearchMgr
from module.result.result_mgr import ResultMgr
from module.selenium.page_gen_mgr import PageGenMgr
from apscheduler.schedulers.background import BlockingScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor


class Operate:

    scheduler = None

    single_exit = False

    @classmethod
    def start(cls):
        # 注册log
        logging.config.dictConfig(log_cfg.get_config())
        instance = cls.get_instance()

        # 初始化调度器, 单线程
        instance.__init_scheduler()
        # 加载配置
        ConfigMgr.boot(cls.scheduler)

        # 页面请求模块
        PageGenMgr.start(cls.scheduler)

        # 结果处理模块
        ResultMgr.start(cls.scheduler)

        # 二次处理模块
        ResearchMgr.start(cls.scheduler)

        # 生产模块
        GenMgr.start(cls.scheduler)

        # 注册ctrl+c退出
        instance.resister_stop()

        cls.scheduler.start()

    @classmethod
    def __init_scheduler(cls):
        executors = {
            'default': ThreadPoolExecutor(20),
            'processpool': ProcessPoolExecutor(5)
        }
        cls.scheduler = BlockingScheduler(executors=executors)

    @staticmethod
    def get_instance():
        return Operate()

    def resister_stop(self):
        signal.signal(signal.SIGINT, self.__handle_ctrl_c)

    def __handle_ctrl_c(self, signal, frame):
        if self.single_exit:
            return
        self.single_exit = True
        GenMgr.stop()
        ResearchMgr.stop()
        ResultMgr.stop()
        PageGenMgr.stop()
        self.scheduler.shutdown(wait=False)
        log_util.com_log.info("app exit")
        sys.exit(0)

    def test(self):
        print("dd")
