#!/usr/bin/python3 
"""
 Author: cg
 Date: 2020/12/17 15:23
"""
from bs4 import BeautifulSoup
from utils import file_util
from utils import request_util
from utils import com_util
from common.headers import headers


url = "https://www.zhipin.com/gongsi/_zzz_c101281600_iy100504/"
# url = "https://www.tianyancha.com/search"

str_cookie = "HMACCOUNT_BFESS=4B972BB450ADE7A9; BDUSS_BFESS=Fh6UmJreXRhS29-WmVZN2l2R2htfkhGN25IWTdYV3lCLUZKQmVTN0MycllYUDVmRVFBQUFBJCQAAAAAAAAAAAEAAAAeXa49WFNZtO25~QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANjP1l~Yz9Zfa; BAIDUID_BFESS=19A7FBCA068C50BC3003363B337E8FA5:FG=1"

# file_path = "D:\\work\\python\\pycharm\\200506\\spiderCompany\\res_page\\boss_zhipin_list.html"
# file_path = "D:\\work\\python\\pycharm\\200506\\spiderCompany\\res_page\\boss_zhipin_company_info.html"
# file_path = "D:\\work\\python\\pycharm\\200506\\spiderCompany\\res_page\\tianya_search_company_list.html"
file_path = "D:\\work\\python\\pycharm\\200506\\spiderCompany\\resource\\page\\tianyan_company_info_new.html"


save_path = "D:\\work\\python\\pycharm\\200506\\spiderCompany\\res_page\\boss_zhipin_list_111.html"


class CompanyInfo:

    # 公司名字
    name = None

    # 法定代表人
    legal = None

    # 电话
    tel = None

    # 成立日期
    establish_date = None

    # 行业
    sector = None

    # 规模
    scope = None

    # 地址
    address = None

    # 经验范围
    business_scope = None

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


def analysis_company_info(page_content):
    soup = BeautifulSoup(page_content, "html.parser")
    info_tag = soup.find("div", class_="job-sec company-business")
    name_tag = info_tag.find("h4")
    if name_tag is None:
        print("未找到")
    company_name = name_tag.get_text()
    full_name = name_tag.contents[1]
    print(company_name)
    print(full_name)


def analysis_tiany_company_searcy_list(page_content):
    soup = BeautifulSoup(page_content, "html.parser")
    container_tags = soup.find("div", class_="result-list sv-search-container")
    item_tags = container_tags.find_all("div", class_="search-item sv-search-company")
    if len(item_tags) <= 0:
        print("未找到")
        return
    result_tag = item_tags[0]
    # print(result_tag.prettify())
    company_name_tag = result_tag.find("div", class_="info")
    company_name = company_name_tag.get_text()
    print(company_name)

    href_tag = result_tag.find("a", class_="name")
    if href_tag is None:
        print("未找到信息")
        return
    href_url = href_tag.get("href")
    print(href_url)


def analysis_tianyan_company_info(page_content):
    soup = BeautifulSoup(page_content, "html.parser")
    contact_tag = soup.find("div", class_="in-block sup-ie-company-header-child-1")
    phone_tag = contact_tag.find("span", class_="label")
    phone_span_tag = phone_tag.next_sibling
    phone_num = phone_span_tag.get_text()
    print(phone_num)

    # 最近更新
    update_tag = soup.find("span", class_="updatetimeComBox")
    print(update_tag.get_text())

    info_tag = soup.find("table", class_="table -striped-col -breakall")
    # print(info_tag.prettify())
    name_tag = info_tag.find("div", class_="name")
    name_a_tag = name_tag.find("a", class_="link-click")
    name = None
    if name_a_tag is None:
        print("法定代表人未找到")
    else:
        name = name_a_tag.get_text()
    print("name: " + name)

    tr_tags = info_tag.find_all("tr")


    # 成立日期
    establish_date = tr_tags[1].contents[1].get_text()
    # 行业
    sector = tr_tags[6].contents[3].get_text()
    # 规模
    scope = tr_tags[6].contents[5].get_text()

    # 地址
    address = tr_tags[9].contents[1].get_text()

    # 经营范围
    business_scope = tr_tags[10].contents[1].get_text()

    print("establish_date: " + establish_date)
    print("sector: " + sector)
    print("scope " + scope)
    print("address " + address)
    print("business_scope " + business_scope)

# cookie_dict = com_util.build_cookie(str_cookie)
# response = request_util.request(url=url, headers=headers, cookie_dict=cookie_dict)
# file_content = response.text
#
# file_util.write_file(save_path, file_content)
file_content = file_util.read_file(file_path)
#
# analysis_company_item(file_content)
# analysis_company_info(file_content)
# analysis_tiany_company_searcy_list(file_content)
analysis_tianyan_company_info(file_content)


# url是否合法
# base_url = request_util.get_base_url("ddd")
# if base_url is None:
#     print("url 不合法")
# print(base_url)


# 测试参数
# dict_params = {
#     "key": "东莞市海达仪器有限公司"
# }
# res_1 = request_util.op_single_rec(url, dict_params, True)
# print("res_1: " + res_1)
#
# res_2 = request_util.op_single_rec(url, dict_params, False)
# print("res_2: " + res_2)
