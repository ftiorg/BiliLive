#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/16 下午 11:22
# @Author  : kamino

import pymysql
import os
import json
from .config import Config


class DbLink(object):

    def __init__(self):
        """初始化"""
        try:
            self.db = pymysql.connect(Config.config('database')['host'], Config.config('database')['user'],
                                      Config.config('database')['password'], Config.config('database')['dbname'])
        except Exception as e:
            print(e)
            exit(0)

    def __del__(self):
        """清理"""
        try:
            self.db.close()
        except Exception as e:
            print(e)

    def query(self, sql=None):
        try:
            self.cursor = self.db.cursor()
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            self.cursor.close()
            return data
        except Exception as e:
            print(e)
            return (None, 'ERROR', str(e))

    def insert(self, sql=None):
        try:
            self.cursor = self.db.cursor()
            self.cursor.execute(sql)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            return False
