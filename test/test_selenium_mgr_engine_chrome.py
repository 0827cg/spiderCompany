#!/usr/bin/python3 
"""
 Author: cg
 Date: 2020/12/31 10:10
"""

from module.selenium.selenium import SeleniumModule
import time

url_1 = "http://www.baidu.com"
url_2 = 'https://httpbin.org/headers'

SeleniumModule.init(False)

time.sleep(2)
print("准备执行请求")

# SeleniumModule.get(url_1, "baidu")


time.sleep(2)

browser = SeleniumModule.get_browser()

browser.execute_script('window.location.href = "http://www.baidu.com";')
SeleniumModule.get(url_2, "headers", False)
# WebDriverWait(browser, 10).until(lambda driver: driver.current_url == url)
# print(browser.page_source)
# print("gg")
# print(SeleniumModule.switch_window_index(0).page_source)
# print('dd')
# print(SeleniumModule.switch_window_index(1).page_source)


print("请求完成")
time.sleep(3)

SeleniumModule.quit()


