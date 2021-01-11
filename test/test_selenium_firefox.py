#!/usr/bin/python3 
"""
 Author: cg
 Date: 2020/12/23 15:41
"""

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import os
import time
from timeit import timeit

driver_path = "D:\\work\\python\\pycharm\\200506\\spiderCompany\\lib\\geckodriver-v0.28.0-win64\\geckodriver.exe"

url_1 = "http://www.baidu.com"
url_2 = "https://cn.bing.com/"
url_3 = "https://www.google.com/"


options = Options()
options.headless = False

browser = webdriver.Firefox(options=options, executable_path=driver_path)
browser.get(url_1)

print("size 1: {}".format(len(browser.window_handles)))

browser.execute_script("window.open('');")

browser.get(url_2)

print("size now: {}".format(len(browser.window_handles)))

for handle in browser.window_handles:
    browser.switch_to.window(handle)
    print("change dddddddd")
    print(browser.page_source)

# browser.switch_to.window(browser.window_handles[1])
# print("dddddddddddddd")

# print(browser.page_source)

print ("Headless Firefox Initialized")

browser.quit()
