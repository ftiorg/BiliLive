#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/26 下午 04:34
# @Author  : kamino

import os
import json


class Config(object):
    CONFIG = {}

    @staticmethod
    def load_config():
        Config.CONFIG['root-path'] = os.path.abspath('.') + '/'
        if not os.path.exists(Config.CONFIG['root-path'] + 'config/config.json'):
            print("NOT FOUND CONFIG FILE")
            exit(0)
        with open(Config.CONFIG['root-path'] + 'config/config.json', 'r', encoding='UTF-8') as f:
            for key, value in json.loads(f.read()).items():
                Config.CONFIG[key] = value
                print("SET %s AS %s" % (key, value))
        return Config.CONFIG

    @staticmethod
    def config(key=None):
        """获取配置项"""
        if key == None:
            return Config.CONFIG
        try:
            value = Config.CONFIG[key]
            return value
        except KeyError:
            return None
