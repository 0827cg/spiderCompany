#!/usr/bin/python3 
"""

 读取保存的cookie

 实现免登录

 Author: cg
 Date: 2020/12/25 17:51
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.firefox.options import Options
import time
from utils import com_util
from utils import file_util

driver_path = "D:\\work\\python\\pycharm\\200506\\spiderCompany\\lib\\geckodriver-v0.28.0-win64\\geckodriver.exe"
save_cookie_path = "D:\\work\\python\\pycharm\\200506\\spiderCompany\\resource\\music_163_cookie.txt"

url_1 = "https://music.163.com/"

options = Options()
options.headless = False

browser = webdriver.Firefox(options=options, executable_path=driver_path)
print("浏览器启动完成")
time.sleep(3)

str_cookie = file_util.read_file(save_cookie_path)
print(str_cookie)
browser.get(url_1)
browser.delete_all_cookies()
list_cookie = com_util.parse_to_dict(str_cookie)

for cookie in list_cookie:
    browser.add_cookie(cookie)

browser.refresh()

