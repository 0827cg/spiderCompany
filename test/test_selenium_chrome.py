#!/usr/bin/python3 
"""
 Author: cg
 Date: 2020/12/30 17:11
"""

# from selenium import webdriver
from seleniumwire import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
import time


chrome_driver_path = "D:\\work\\python\\pycharm\\200506\\spiderCompany\\lib\\chromedriver_win32\\chromedriver.exe"

url_1 = "http://www.baidu.com"

referer = "https://www.bing.com/"

options = Options()
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
webdriver.ChromeOptions()

browser = webdriver.Chrome(options=options, executable_path=chrome_driver_path)
print("浏览器启动完成")
time.sleep(3)


# browser.execute_script('window.location.href = "{}";'.format(referer))
# browser.get(url_1)
# browser.get("javascript: window.location.href = '{}'".format(url_1))

browser.header_overrides = {
    'Referer': 'http://www.baidu.com',
}

# browser.


url = 'https://httpbin.org/headers'
browser.get(url)
browser.implicitly_wait(10)
# WebDriverWait(browser, 10).until(lambda driver: driver.current_url == url)
print(browser.page_source)


print("请求完成")
time.sleep(6)
# for request in browser.requests:
#   print(request.url) # <--------------- Request url
#   print(request.headers) # <----------- Request headers
#   print(request.response.headers) # <--

browser.quit()
