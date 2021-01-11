#!/usr/bin/python3 
"""

 测试cookie



 Author: cg
 Date: 2020/12/29 9:30
"""

from module.selenium.selenium import SeleniumModule
import time

music_url = "https://music.163.com/"
music_cookie_path = "D:\\work\\python\\pycharm\\200506\\spiderCompany\\resource\\music_163_cookie.txt"

tianyan_url = "https://www.tianyancha.com"
tianyan_cookie_path = "D:\\work\\python\\pycharm\\200506\\spiderCompany\\resource\\tianyancha_cookie.txt"


SeleniumModule.init(False)

time.sleep(2)
print("准备执行请求")


SeleniumModule.site_add_cookies("boss", music_url, "boss_url", music_cookie_path)

print("music url complete")
time.sleep(3)

SeleniumModule.site_add_cookies("tianyan", tianyan_url, "tianyan_url", tianyan_cookie_path)

print("tianyan complete")

music_url_1 = "https://music.163.com/#/friend"

# suc = SeleniumModule.switch_window("boss_url")
# if suc:
#     print("switch success")
# print("switch")

# 测试得出新开一个同网站的窗口, cookie开始会记录
SeleniumModule.get(music_url_1, "music_url_2")
