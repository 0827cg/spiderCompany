#!/usr/bin/python3 
"""

 保存music.163.com这个网站上面的登录后的cookie

 启动程序后

 在打开的浏览器中登录账户

 35秒后, 程序执行保存cookie到save_cookie_path这个文件中

 用以后面的程序来读取该cookie, 实现cookie登录, 而不用编写输入账户密码的操作

 Author: cg
 Date: 2020/12/25 16:57
"""

from selenium import webdriver
# from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.options import Options
import time
from utils import com_util
from utils import file_util

firefox_driver_path = "D:\\work\\python\\pycharm\\200506\\spiderCompany\\lib\\geckodriver-v0.28.0-win64\\geckodriver.exe"
chrome_driver_path = "D:\\work\\python\\pycharm\\200506\\spiderCompany\\lib\\chromedriver_win32\\chromedriver.exe"
# save_cookie_path = "D:\\work\\python\\pycharm\\200506\\spiderCompany\\resource\\music_163_cookie.txt"
save_cookie_path = "D:\\work\\python\\pycharm\\200506\\spiderCompany\\resource\\music_163_cookie_chrome.txt"

url_1 = "https://music.163.com/"

options = Options()
options.headless = False

options.add_experimental_option('useAutomationExtension', False)
# 为实现window.navigator.webdriver为null, 第二个有用对我
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_argument("--disable-blink-features=AutomationControlled")

options.add_argument("--disable-blink-features")
options.add_argument("--disable-blink-features=AutomationControlled")

# 取消错误日志
options.add_experimental_option("excludeSwitches", ["enable-logging"])

# browser = webdriver.Firefox(options=options, executable_path=firefox_driver_path)
browser = webdriver.Chrome(options=options, executable_path=chrome_driver_path)
print("浏览器启动完成")
time.sleep(3)


browser.get(url_1)

time.sleep(35)

dict_cookie = browser.get_cookies()
str_cookie = com_util.parse_to_json(dict_cookie)

file_util.write_file(save_cookie_path, str_cookie)
