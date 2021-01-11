#!/usr/bin/python3 
"""
 Author: cg
 Date: 2020/12/31 11:16
"""

from seleniumwire import webdriver
import time

chrome_driver_path = "D:\\work\\python\\pycharm\\200506\\spiderCompany\\lib\\chromedriver_win32\\chromedriver.exe"

url_1 = "http://www.baidu.com"

referer = "https://www.bing.com/"

options = webdriver.ChromeOptions()
options.headless = False

options.add_experimental_option('useAutomationExtension', False)
# 为实现window.navigator.webdriver为null, 第二个有用对我
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_argument("--disable-blink-features=AutomationControlled")

options.add_argument("--disable-blink-features")
options.add_argument("--disable-blink-features=AutomationControlled")

# 取消错误日志
# options.add_experimental_option("excludeSwitches", ["enable-logging"])


# options.add_argument("--referer=" + referer)

browser = webdriver.Chrome(options=options, executable_path=chrome_driver_path)

# browser.header_overrides = {
#     'Referer': 'http://www.baidu.com',
# }

def add_headers(k, v):
    browser.header_overrides = {
        k: v
    }

add_headers('Referer', "http://www.baidu.com")
add_headers('Referer', "http://www.baidudd.com")


print("揿动完成")
time.sleep(3)
browser.get("https://httpbin.org/headers")
print("加载完成")
print(browser.page_source)

print("请求完成")
browser.quit()
