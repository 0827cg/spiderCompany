#!/usr/bin/python3 
"""

 分配给所有research去执行搜索


 Author: cg
 Date: 2020/12/18 11:36
"""

from queue import Queue
from module.config_mgr import ConfigMgr
from module.generate.gen_msg import GenMsg
from module.research.tianyan_cha.tianyan_mgr import TianyanChaMgr
from utils import log_util


class ResearchMgr:

    # 所有的待搜索的消息
    __queue = Queue(maxsize=0)

    @classmethod
    def start(cls, scheduler):
        TianyanChaMgr.start(scheduler)
        # 每100毫秒从中取出
        scheduler.add_job(cls.run, 'interval', seconds=1)
        log_util.com_log.info("ResearchMgr started...")

    @classmethod
    def stop(cls):
        TianyanChaMgr.stop()
        log_util.com_log.info("stop ResearchMgr")

    @classmethod
    def run(cls):
        if cls.__queue.empty():
            return
        msg = cls.__queue.get_nowait()
        if msg is None:
            return
        try:
            cls._assign_search(msg)
        except BaseException as error:
            log_util.err_log.error("execute func error: {}".format(error))

    @classmethod
    def put(cls, msg):
        if not isinstance(msg, GenMsg):
            return
        cls.__queue.put(msg)

    @classmethod
    def _assign_search(cls, msg):
        TianyanChaMgr.handle_search(msg.name, msg.category)
