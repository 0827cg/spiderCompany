#!/usr/bin/python3 
"""

 使用selenium来保存cookie

 Author: cg
 Date: 2020/12/25 18:08
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os
from utils import com_util
from utils import file_util

# 请求的url
url = "https://www.tianyancha.com/"
# 保存cookie的文件名, 后缀为txt
name = "tianyancha_cookie_chrome"


chrome_driver_path = "D:\\work\\python\\pycharm\\200506\\spiderCompany\\lib\\chromedriver_win32\\chromedriver.exe"
save_cookie_dir = "D:\\work\\python\\pycharm\\200506\\spiderCompany\\resource\\"


options = Options()
options.headless = False


options.add_experimental_option('useAutomationExtension', False)
# 为实现window.navigator.webdriver为null, 第二个有用对我
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_argument("--disable-blink-features=AutomationControlled")

options.add_argument("--disable-blink-features")
options.add_argument("--disable-blink-features=AutomationControlled")


browser = webdriver.Chrome(options=options, executable_path=chrome_driver_path)
print("浏览器启动完成")
time.sleep(3)

browser.get(url)

time.sleep(50)

print("等待结束, 执行保存cookie")

dict_cookie = browser.get_cookies()
str_cookie = com_util.parse_to_json(dict_cookie)

file_name = name + ".txt"
save_cookie_path = os.path.join(save_cookie_dir, file_name)

file_util.write_file(save_cookie_path, str_cookie)
print("cookie已保存")
