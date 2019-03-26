#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/26 下午 10:41
# @Author  : kamino

import time


class Timer(object):
    @staticmethod
    def timestamp():
        """返回时间戳"""
        return int(time.time())

    @staticmethod
    def str2stamp(s, format='%Y-%m-%d %H:%M:%S'):
        """时间字符串转时间戳"""
        return int(time.mktime(time.strptime(s, format)))
