#!/usr/bin/python3 
"""
 Author: cg
 Date: 2020/12/18 14:46
"""

import os
from queue import Queue
from utils import log_util
from utils import com_util
from utils import file_util
from module.config_mgr import ConfigMgr
from module.research.tianyan_cha.tianyan_result import TianyanResult


class ResultMgr:

    # 存放结果的队列
    __queue = Queue(maxsize=0)

    # 已经保存的数量
    __save_num = 0

    @classmethod
    def start(cls, scheduler):
        # 每100毫秒尝试从中取出
        scheduler.add_job(cls.run, 'interval', seconds=1)
        log_util.com_log.info("ResultMgr started...")

    @classmethod
    def stop(cls):
        log_util.com_log.info("stop ResultMgr")

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
        # 暂时用TianyanResult这个结构
        if not isinstance(msg, TianyanResult):
            return
        cls.__queue.put(msg)

    @classmethod
    def _assign_search(cls, msg):
        save_dir = ConfigMgr.get_config("base").outDirPath
        save_dir = os.path.join(save_dir, msg.category)
        c_name = msg.name
        res = com_util.write_to_json_dir(msg.__dict__, save_dir, c_name)
        if res:
            if cls.__save_num <= 0:
                log_util.com_log.info("save json dir path: {}".format(save_dir))
            log_util.com_log.info("json file: {}.json".format(c_name))
        cls.__save_num += 1
