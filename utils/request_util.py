#!/usr/bin/python3
"""
 打包的requests网络请求, 目前只实现了get/post的请求
 另外
 增加了依靠定义的dict类型的url信息来进行请求操作, 同时包含对结果的分析, 数据的赋值操作
 dict格式
 {
     "id": xx                       仅标识
     "method": "GET"/"POST"         http方法, 默认GET
     "url": xxx                     请求的url, 如果url中存在"{}"包裹的字符串, 则需要将其字符串作为key从const_cls中取值
                                    重新构造url,
                                    同时也可以使用'@'作为开头来从const_cls中取值
     "headers": {}                  请求前需要增加的header属性, key: header中的key, value: 字符串, 如果字符串以@开头
                                    则后面的字符串则为从const_cls中的属性名字, 从中取
     "rmHeaders": []                需要删除的headers, key
     "params": {}                   参数, dict,无则不需要设置, 如value中存在"@"开头的, 则是需要从const_cls中取数据
     "single": true/false           dict参数的在url 编码时 用引号用单引号(%27)还是双引号(%22), 这里表示是否为单引号, 默认true
     "data": xx                     通常用在二机制数据, post上传媒体文件
     "json": xx                     这个值也是作为post函数 提交表单dict类型数据的时候用到的, dict中的value若以'@'开头则从const_cls中取值
                                    同时也dict可认为与params一样的配置效果, list也可
     "sleep": xx                    执行此请求前休眠xx秒(最好不要大于10秒)
     "success": {}                  数据成功标识(只包含一组key,value), 仅用到返回json格式时,
                                    非json格式则只根据http的放回值判断是否为200
                                    ["key", "value"], key可包含".", 其中,当value为"not none"时, 则表示该key值不能为空

                                    根据key匹配返回的数据中的value是否对得上， '.'号连接表示多重
     "setReferer": True/False       是否将当前url设置到request header中的Referer属性中, 默认False
     "assign": {}                   读取结果, 并赋值到调用的函数analysis_request中的参数const_cls中,
                                    如果需要赋值, 需要注意const_cls只能为类对象,
                                    assign配置的值可以为dict/list
                                    dict: assign的key: key: const_cls中的属性名字, value: 请求返回的结果中的key, '.'号连接表示多重
                                    返回数据无需记录保存则不用设置此字段
                                    如与list, 示例: xxx.xxx[2].xxx
                                    list: 长度最大只接受3，[x, y, z] x: 赋值来自response, y赋值来自response.content, z: response.text
                                    x,y都是const_cls中的属性名字
     "execute": []                  请求完成之后, 需要执行的函数名字集合, 元素为str, 函数来自const_cls对象中的函数
 }
 Author: cg
 Date: 2020/8/21 14:01
"""

import requests
import json
import time
from urllib import parse
from utils import com_util
from utils import log_util
from utils import string_util


# 单次请求超时时间, 秒
outTime = 15
logger = log_util.com_log
err_logger = log_util.err_log


def analysis_request(url_dict, headers, cookie_dict, const_cls=None):
    """
    分析url_dict数据, 并执行请求
    :param url_dict: 至于内容及其含义, 文件开头的描述
    :param headers:
    :param cookie_dict:
    :param const_cls: 用来存放属性的类(类对象中的属性接收赋值),
    :return: res, type为dict 表示执行成功, 且未出错, None: 出错
    """
    if url_dict is None or not isinstance(url_dict, dict):
        err_logger.error("type of url_dict unreasonable")
        return

    if const_cls is not None and not isinstance(const_cls, object):
        err_logger.error("type of const_cls unreasonable")
        return

    method = url_dict.get("method")
    url = url_dict.get("url")
    params = url_dict.get("params")
    single = url_dict.get("single")
    data = url_dict.get("data")
    data_json = url_dict.get("json")
    add_headers = url_dict.get("headers")
    rm_headers = url_dict.get("rmHeaders")
    sleep = url_dict.get("sleep")
    success = url_dict.get("success")
    set_referer = url_dict.get("setReferer")
    assign = url_dict.get("assign")
    execute = url_dict.get("execute")

    if url is None or not url:
        return

    # url检测构造
    url = op_url(url, const_cls)
    if url is None:
        err_logger.error("url is none")
        return

    # 检测是否有需要增加的header
    op_headers(headers, const_cls, add_headers)

    # 检测赋值参数
    op_params(params, const_cls)

    # 检测是否需要对url进行自定义url编码, 效果看op_single_rec方法
    # 若这里已经将params参数合并到url中, 那么requests里面将不会在对params进行url合并更改
    url = op_single_rec(url, params, single)

    # 检测提交的数据
    data = op_data(data, const_cls)

    # 检测data_json
    op_data_json(data_json, const_cls)

    # 检测是否休眠
    op_sleep(sleep)

    if method is None or method is "GET":
        res = request(url, params, data, None, headers, cookie_dict)
    else:
        res = request(url, params, data, data_json, headers, cookie_dict, False)

    # 检测是否成功
    suc = op_success(res, success)
    if not suc:
        err_logger.error("occur fail when request, url: {}".format(url))
        return

    if set_referer is not None and set_referer is True:
        headers['Referer'] = url

    # 测试给const_cls赋值
    op_assign(res, const_cls, assign)

    # 检测请求完后执行
    op_execute(execute, const_cls)
    return res


def request(url, params=None, data=None, data_json=None, headers=None, cookie_dict=None, is_get=True,
            check_params=True):
    """
    get/post 请求
    :param url: url
    :param params: 参数, dict
    :param data: 数据
    :param data_json: dict数据
    :param headers: header, dict
    :param cookie_dict: 如果不需要带cookie, 则可设为None
    :param is_get: 是否使用get方法去请求, 默认True
    :param check_params: 是否检测参数, url, headers, cookie
    :return: 返回response, None: 失败
    """
    if check_params:
        check_res = check_request_params(url, headers, cookie_dict)
        if not check_res:
            return

    try:
        if is_get:
            res = requests.get(url, params=params, data=data, headers=headers, cookies=cookie_dict, timeout=outTime)
        else:
            res = requests.post(url, params=params, data=data, json=data_json, headers=headers, cookies=cookie_dict,
                                timeout=outTime)

    except requests.exceptions.Timeout:
        err_logger.error("request timeout, url: {}".format(url))
        return

    except requests.exceptions.RequestException as e:
        err_logger.error("request error, url: {}, error: {}".format(url, e))
        return

    if res.status_code != 200:
        err_logger.error("request url fail, url: {}, status_code: {}".format(url, res.status_code))
        return
    return res


def op_url(url, const_cls):
    """
    构造url, 如果url中包含有"{}"这类符号所包裹着字符串, 则表示需要将其作为key从const_cls中取值替换
    :param url: str url
    :param const_cls: 保存参数值的类对象
    :return: 返回完整的url
    """
    if url is None or not url or not isinstance(url, str):
        return None

    if const_cls is None or not isinstance(const_cls, object):
        return url

    if url.find("@") != -1:
        str_key = url.split("@")[1]
        url = const_cls.__getattribute__(str_key)
        return url

    while True:
        b_index = url.find("{")
        if b_index == -1:
            break
        e_index = url.find("}")
        key = url[b_index + 1:e_index]
        if key:
            value = const_cls.__getattribute__(key)
        else:
            value = str()
        need_replace = "{" + key + "}"

        if value is None:
            err_logger.error("the value of key in const_cls is none, key: {}".format(key))
            return None
        url = url.replace(need_replace, value)
    return url


def op_params(params_dict, const_cls):
    """
    构造参数, dict类型, 对value中由"@"开头的字符串进行重新赋值, 作为key从const_cls中获取
    :param params_dict:
    :param const_cls:
    :return:
    """
    if params_dict is None or not isinstance(params_dict, dict):
        return

    if not params_dict:
        return
    for key, value in params_dict.items():
        # if not key or not isinstance(value, str):
        #     continue

        if value is None:
            value = str()

        if isinstance(value, list):
            new_value = list()
            for item in value:
                if isinstance(item, str) and item.find("@") != -1:
                    str_key = item.split("@")[1]
                    item = const_cls.__getattribute__(str_key)
                    new_value.append(item)
                else:
                    new_value.append(item)
            params_dict.update({key: new_value})

        if isinstance(value, dict):
            op_params(params_dict.get(key), const_cls)

        if isinstance(value, str):
            value_arr = value.split("@")
            if len(value_arr) <= 1:
                continue
            update_dict = {key: const_cls.__getattribute__(value_arr[1])}
            params_dict.update(update_dict)

        # 最后将value为dict的转换成str
        # if isinstance(value, dict):
        #     params_dict.update({key: str(value)})


def op_single(params_dict, single):
    """
    将params_dict转换单双引号(dict转json字符串, 双引号)
    :param params_dict:
    :param single: 是否为单引号, 默认True
    :return: 返回新的params
    """
    if not isinstance(params_dict, dict):
        return params_dict
    if single is None or single is True:
        # 单引号
        return params_dict
    params_str = com_util.parse_to_json(params_dict)
    return params_str


def op_single_rec(url, params_dict, single):
    """
    直接看场景,  url: "https://mp.toutiao.com/xigua/api/upload/getAuthKey/"
                params_dict = {params={"type":"video","column":false,"ugc":false}

    如果single为false:
    则url编码后的url为:
    https://mp.toutiao.com/xigua/api/upload/getAuthKey/?params=%7B%22type%22%3A%22video%22%2C%22column%22%3Afalse%2C%22ugc%22%3Afalse%7D

    而如果为true(requests模块自己组装url):
    被其url编码后url为:
    https://mp.toutiao.com/xigua/api/upload/getAuthKey/?params=%7B%27type%27%3A+%27video%27%2C+%27column%27%3A+False%2C+%27ugc%27%3A+False%7D

    :param url:
    :param params_dict:
    :param single:
    :return:
    """
    if not isinstance(params_dict, dict):
        return url
    if single is None or single is True:
        return url
    url_params = str()
    for key, value in params_dict.items():
        if isinstance(value, dict):
            value = com_util.parse_to_json(value)
        url_params = url_params + key + "=" + value + "&"
    url_params = url_params[0:-1]
    url_params = parse.quote(url_params, safe="=")
    res_url = url + "?" + url_params
    return res_url


def op_data(data, const_cls):
    """
    这里提交的data， 尽量只为str, list, 二进制
    dict不走这
    :param data:
    :param const_cls:
    :return:
    """
    if isinstance(data, str):
        index = data.find("@")
        if index == -1:
            return data

        key = data[index + 1:]
        data = const_cls.__getattribute__(key)

    if isinstance(data, list):
        for item in data:
            op_params(item, const_cls)
    return data


def op_data_json(data, const_cls):
    """
    data数据, 如果是字符串且存在'@', 那么从const_cls中取, 并返回
    如果是dict, 则跟params一样
    :param data:
    :param const_cls:
    :return: data
    """
    data = op_data(data, const_cls)
    op_params(data, const_cls)


def op_headers(headers_dict, const_cls, add_header):
    """
    将add_header这个dict里面的key和对应的value增加到headers_dict中
    :param headers_dict:
    :param const_cls:
    :param add_header: key: 增加的header名字, value: 值, 若以@开头, 则将认为时const_cls中的属性名
    :return:
    """
    if add_header is None or not isinstance(add_header, dict) or not add_header:
        return

    if headers_dict is None or not isinstance(headers_dict, dict):
        return

    if const_cls is None or not isinstance(const_cls, object):
        return

    for key, value in add_header.items():
        if key is None or not key:
            continue
        if value is None:
            value = str()
        value_arr = value.split("@")
        if len(value_arr) <= 1:
            headers_dict[key] = value
            continue

        if not value_arr[1]:
            err_logger.error("index 1 is none when value: {} to split".format(value))
            return
        re_value = const_cls.__getattribute__(value_arr[1])
        headers_dict[key] = re_value


def op_sleep(sleep):
    """
    执行休眠一段时间
    :param sleep: 秒
    :return:
    """
    if sleep is None or not isinstance(sleep, int):
        return
    logger.info("sleep waiting {} seconds before that request".format(sleep))
    time.sleep(sleep)


def op_success(response, success_list):
    """
    匹配success_list中的key对应的value是否和response.text中的key的value是否相同
    :param response:
    :param success_list: [key, value]
    :return: true: 相同
    """
    if response is None or not isinstance(response, requests.Response):
        err_logger.error("response is empty or type unreasonable")
        return False

    if not _is_json(response) or success_list is None or not isinstance(success_list, list):
        logger.info("request success, url: {}, code: {}".format(response.url, response.status_code))
        return True

    if len(success_list) != 2:
        err_logger.error("the check whether success value is unreasonable, success_list: {}".format(success_list))
        return False
    res_dict = json.loads(response.text)
    key_str = success_list[0]
    value_str = success_list[1]
    op_res = get_value_from_dict(res_dict, key_str)
    if value_str == "not none":
        if op_res is None or not op_res:
            err_logger.error("request url fail , url: {}, response.text: {}".format(response.url, response.text))
            return False
        else:
            logger.info("request success, url: {}".format(response.url))
            return True

    if op_res is None:
        err_logger.error("key_str: {} not found value in response of url: {} , response.text: {}".format(
            key_str, response.url, response.text))
        return False

    if op_res == value_str:
        logger.info("request success, url: {}".format(response.url))
        return True
    else:
        err_logger.error("request url fail , url: {}, response.text: {}".format(response.url, response.text))
        return False


def op_assign(response, const_cls, assign):
    """
    从res_dict中取值, 为const_cls类中的属性赋值
    :param response: 响应
    :param const_cls: object  类
    :param assign: 如果是dict, 那么: key: const_cls中的属性名字, value: res_dict中的key
                    也可以是list(元素str), index: 0时赋值response.content, 1时赋值response.text
    :return: None
    """
    if response is None or not isinstance(response, requests.Response):
        return

    if const_cls is None or not isinstance(const_cls, object):
        return

    if not _is_json(response):
        # 处理非json
        _op_assign_list(response, const_cls, assign)
        return

    res_text = response.text
    if res_text is None or not res_text:
        return
    res_dict = json.loads(res_text)

    if assign is None or not assign:
        return

    if isinstance(assign, list):
        _op_assign_list(response, const_cls, assign)
        return

    if not isinstance(assign, dict):
        return

    for key, value in assign.items():
        res_value = get_value_from_dict(res_dict, value)
        if value is None:
            continue
        const_cls.__setattr__(key, res_value)


def _op_assign_list(response, const_cls, assign):
    """
    处理当assign为list时的赋值
    :param response:
    :param const_cls:
    :param assign:
    :return:
    """
    if not isinstance(assign, list):
        return

    index = 0
    for item in assign:
        index += 1
        if not isinstance(assign[0], str):
            continue

        if item is "_":

            continue

        if index == 1:
            const_cls.__setattr__(item, response)
        elif index == 2:
            const_cls.__setattr__(item, response.content)
        elif index == 3:
            const_cls.__setattr__(item, response.text)

    if len(assign) <= 1:
        if isinstance(assign[0], str):
            if assign[0] is "_":
                return
            const_cls.__setattr__(assign[0], response)
        return


def op_execute(execute, const_cls):
    """
    执行对象函数
    :param execute:
    :param const_cls:
    :return:
    """
    if execute is None or not isinstance(execute, list):
        return
    if const_cls is None or not isinstance(const_cls, object):
        return
    for func_name in execute:
        com_util.execute_method(const_cls, func_name)


def get_value_from_dict(res_dict, key_str):
    """
    根据字符串从dict中获取对应的value, 字符串用'.'连接表示多重key
    :param res_dict:
    :param key_str:
    :return: str, None: 无
    """
    if not isinstance(res_dict, dict):
        return

    if not isinstance(key_str, str):
        return

    if not res_dict or not key_str:
        return

    key_arr = key_str.split(".")
    if len(key_arr) == 1:
        return res_dict.get(key_str)

    op_res = res_dict.copy()

    try:
        for key in key_arr:

            if key.find("[") == -1:
                op_res = op_res.get(key)
                continue
            index = key.find("[")
            dict_key = key[0:index]
            num = int(key[index + 1:key.find("]")])
            if not isinstance(op_res.get(dict_key), list):
                return
            op_res = op_res.get(dict_key)[num]
            # if key.find("[") != -1:
            # op_res = op_res.get(key)
    except Exception as e:
        err_logger.error("error: {}".format(e))
        return
    return op_res


def check_request_params(url, headers, cookie_dict, check_url=False):
    """
    判断url, headers, cookie参数是否合法
    :param url:
    :param headers:
    :param cookie_dict:
    :param check_url: 是否需要检测url
    :return: true: 通过
    """

    if check_url:
        if not isinstance(url, str):
            err_logger.error("type of url unreasonable, url: {}".format(url))
            return False

    if not isinstance(headers, dict):
        err_logger.error("type of headers unreasonable, url: {}".format(headers))
        return False

    if cookie_dict is not None and not isinstance(cookie_dict, dict):
        err_logger.error("type of cookie_dict unreasonable, url: {}".format(cookie_dict))
        return False
    return True


def _is_json(response):
    con_type = response.headers.get("Content-Type")
    json_index = con_type.find("application/json")
    if json_index != -1:
        return True
    return con_type.find("plain") != -1


def get_base_url(url):
    """
    根据url返回协议和域名
    :param url:
    :return: None: url不合法
    """
    parse_res = parse.urlparse(url)
    scheme = parse_res.scheme
    netloc = parse_res.netloc
    if string_util.is_empty(scheme) or string_util.is_empty(netloc):
        return None
    return scheme + "://" + netloc
