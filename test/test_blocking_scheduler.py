#!/usr/bin/python3 
"""
 Author: cg
 Date: 2020/12/16 15:44
"""

import signal
import sys
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
import threading


class ModuleA:

    @classmethod
    def run(cls):
        print("moduleA run")
        instance = cls.get_instance()
        instance.test()

    @staticmethod
    def test():
        print("moduleA test")

    @staticmethod
    def get_instance():
        return ModuleA()


class ModuleB:

    @classmethod
    def run(cls):
        print("moduleB run")
        instance = cls.get_instance()
        instance.test()

    @staticmethod
    def test():
        print("moduleB test")

    @staticmethod
    def get_instance():
        return ModuleB()


class Test:
    scheduler = None

    def run(self):
        executors = {
            'default': ThreadPoolExecutor(20),
            'processpool': ProcessPoolExecutor(5)
        }
        self.prepare_run()
        self.register_stop()
        self.scheduler = BlockingScheduler(executors=executors, daemonic=True)
        self.scheduler.add_job(ModuleA.run, 'interval', seconds=2)
        self.scheduler.add_job(ModuleB.run, 'interval', seconds=3)
        self.scheduler.start()
        print("启动完成")

    def prepare_run(self):
        print("准备启动")

    def show(self):
        print("ddd")

    @classmethod
    def test(cls):
        instance = cls.get_instance()
        instance.run()

    @staticmethod
    def get_instance():
        return Test()

    def register_stop(self):
        signal.signal(signal.SIGINT, self.handle_ctrl_c)

    def handle_ctrl_c(self, signal, frame):
        print("Got ctrl+c, going down!")
        self.scheduler.shutdown()
        sys.exit(0)


Test.test()
