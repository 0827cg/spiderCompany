#!/usr/bin/python3 
"""
 Author: cg
 Date: 2020/12/21 14:03
"""

from bs4 import BeautifulSoup
import requests
from common.headers import headers
from utils import file_util


save_path = "D:\\work\\python\\pycharm\\200506\\spiderCompany\\res_page\\boss_zhipin_list_save.html"

# url = "https://www.zhipin.com/gongsi/_zzz_c101281600_iy100504/"
url = "https://cn.bing.com/"
# url = "https://www.zhipin.com/gongsi/_zzz_c101281600_iy100504/?srcReferer=https://www.zhipin.com/web/common/security-check.html?seed=nJNEIYKnC7%2BIbVJX0J2qimGFUIkDH3VJCt9lV0PeKlg%3D&name=f52d7850&ts=1608530689816&callbackUrl=%2Fgongsi%2F_zzz_c101281600_iy100504%2F&srcReferer="
# url = "https://www.zhipin.com/web/common/security-check.html?seed=nJNEIYKnC7%2BIbVJX0J2qiqEk9%2FTl%2FXMWTYGOKfW3eS4%3D&name=6dec230b&ts=1608707038113&callbackUrl=%2Fgongsi%2F_zzz_c101281600_iy100504%2F&srcReferer="

def analysis_company_item(page_content):
    soup = BeautifulSoup(page_content, "html.parser")

    selected_tag = soup.find_all("span", class_="dropdown-select selected")
    category = str()
    for item in selected_tag:
        if item is None:
            continue
        item = item.get_text().replace('/', '+')
        category += item
    print(category)



    tag = soup.find("div", class_="company-tab-box company-list")
    item_tags = tag.find_all("div", class_="sub-li")
    print(len(item_tags))
    for item in item_tags:
        a_tag = item.find("a", class_="company-info")
        item_href = a_tag.get("href")
        print(item_href)
    # print(tag)
    # print(type(tag))
    next_tag = tag.find("a", class_="next")
    if next_tag is not None:
        next_href = next_tag.get("href")
        print("next_href: " + next_href)


def show_dict(dict_value):
    if not isinstance(dict_value, dict):
        print("not dict type")
        # return
    for k, v in dict_value.items():
        print("{}: {}".format(k, v))

# request

response = requests.get(url=url, headers=headers)
code = response.status_code
history_res = response.history
text = response.text

print("response code: " + str(code))
file_util.write_file(save_path, text)
print("response headers")
show_dict(response.headers)

for item in history_res:
    print("history url: {}".format(item.url))
    print("history code: {}".format(item.status_code))
    print("history response headers 如下")
    show_dict(headers)


# analysis_company_item(text)

