#!/usr/bin/python3 
"""
 Author: cg
 Date: 2020/12/16 15:22
"""


import time
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler



def show():
    print("dd")

def doShow():
    print("doShow")

def sleep_show():
    print("主进程等待10s")
    time.sleep(10)
    print("主进程等待20s完毕")

class DoTest:

    def __init__(self):
        self.bScheduler = BackgroundScheduler()
        self.bScheduler.add_job(show, 'interval', seconds=0.1)
        self.bScheduler.start()


    def test(self):

        self.bScheduler.add_job(doShow, 'interval', seconds=2)
        print('main')
        sleep_show()

DoTest().test()