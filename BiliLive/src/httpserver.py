#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/15 下午 11:17
# @Author  : kamino

from flask import Flask
from .error import Error


class HttpServer(object):

    def run(self):
        """初始化"""
        try:
            self.app = Flask(__name__)
        except Exception as e:
            print(e)
            exit(0)
