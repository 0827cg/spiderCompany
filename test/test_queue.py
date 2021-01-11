#!/usr/bin/python3 
"""
 Author: cg
 Date: 2020/12/17 18:03
"""
import time
from queue import Queue

queue = Queue(maxsize=0)


def show():
    print("ddd")


def test():
    print("test")

queue.put(show())
queue.put(test())


while True:
    func_item = queue.get()
    if func_item is None:
        time.sleep(2)
        break
    func_item()
    # queue.task_done()
    time.sleep(1)

print("over")