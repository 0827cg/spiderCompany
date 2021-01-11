#!/usr/bin/python3 
"""
 Author: cg
 Date: 2020/12/31 15:04
"""
import logging

class TestObj:

    age = 10

    def show(self):
        print("TestObj show age: {}".format(self.age))

def test_exception(test):
    test.show()
    test.cal()

def run():
    test = TestObj()
    try:
        test_exception(test)
    except BaseException as err:
        print(err)
        logging.info(err)
        logging.exception(err)

run()