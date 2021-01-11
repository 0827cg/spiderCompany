#!/usr/bin/python3 
"""
 Author: cg
 Date: 2020/12/16 14:28
"""
from common.schema.config.abstract import Abstract
from utils import com_util
from utils import log_util
from utils import string_util
from common.const import confDirName
import os
import json


class ConfigMgr:

    # key: file name, value: obj
    __config_obj = dict()

    @staticmethod
    def get_instance():
        return ConfigMgr()

    @classmethod
    def boot(cls, scheduler):
        instance = cls.get_instance()
        configs = Abstract.__subclasses__()
        for item in configs:
            cls.__boot_single(item)
        log_util.com_log.info("configuration boot complete")

    @classmethod
    def __boot_single(cls, item):
        """
        加载单个配置
        不存在则初始化
        :param item: 类名
        :return:
        """
        file_name = item.__name__
        file_name = string_util.lowers_first(file_name)
        dir_path = cls.get_config_dir()
        json_file_path = com_util.create_file_path_json(dir_path, file_name)
        exist = com_util.check_file_exist(json_file_path)
        if exist:
            value = com_util.read_from_json(json_file_path)
            obj_item = com_util.parse_to_obj(value, item)
            cls.__config_obj[file_name] = obj_item
            return
        obj_item = item()
        obj_item.init_def()
        json_data = com_util.parse_obj_to_json(obj_item, True)
        com_util.write_to_json(json_data, json_file_path)
        cls.__config_obj[file_name] = obj_item

    @staticmethod
    def get_config_dir():
        return os.getcwd() + os.sep + confDirName

    @classmethod
    def get_config(cls, name):
        value = cls.__config_obj[name]
        if value is None or not value:
            log_util.err_log.error("config unreasonable, file name: {}".format(name))
            return None
        return cls.__config_obj[name]
