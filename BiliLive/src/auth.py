#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/26 下午 09:54
# @Author  : kamino

import requests
import json
from .config import Config


class Auth(object):
    @staticmethod
    def get_cookie():
        """
        放弃使用,过不了csrf验证
        获取cookie的函数
        我这直接用的BilibiliHepler获取的cookie
        :return:
        requests的cookie
        """
        return None