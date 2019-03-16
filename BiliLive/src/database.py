#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/16 下午 11:22
# @Author  : kamino

import pymysql
import os
import json


class DbLink(object):

    def __init__(self):
        """初始化"""
        try:
            with open(os.path.abspath('.') + '/config/config.json', 'r') as f:
                conf = json.loads(f.read())
                self.db = pymysql.connect(conf['database']['host'], conf['database']['user'],
                                          conf['database']['password'], conf['database']['dbname'])
        except Exception as e:
            print(e)

    def __del__(self):
        """清理"""
        try:
            self.db.close()
        except Exception as e:
            print(e)

    def execute(self, sql=None):
        try:
            self.cursor = self.db.cursor()
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            self.cursor.close()
            return data
        except Exception as e:
            print(e)
            return None
