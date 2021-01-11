#!/usr/bin/python3 
"""
 Author: cg
 Date: 2020/12/16 17:02
"""

import threading


class ThreadA(threading.Thread):

    def __init__(self, thread_id):
        threading.Thread.__init__(self)

    def run(self):
        print("run")


print("prepare start thread")
thread_a = ThreadA(1)
thread_a.start()
thread_a.join()