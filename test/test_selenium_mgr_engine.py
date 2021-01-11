#!/usr/bin/python3 
"""
 Author: cg
 Date: 2020/12/25 10:18
"""

from module.selenium.selenium import SeleniumModule
import time

url_1 = "http://www.baidu.com"
url_2 = "https://cn.bing.com/"
url_3 = "https://www.google.com/"

SeleniumModule.init(False)

time.sleep(2)
print("准备执行请求")

SeleniumModule.get(url_3, "google")

SeleniumModule.get(url_1, "baidu")

time.sleep(3)


time.sleep(3)

SeleniumModule.get(url_2, "bing")

SeleniumModule.close_tab("google")

print("size: {}".format(len(SeleniumModule.get_browser().window_handles)))

time.sleep(4)

print(SeleniumModule.get_page_source("baidu"))

print("ddd")

print(SeleniumModule.get_page_source("bing"))


print("over")

time.sleep(3)

SeleniumModule.quit()
