#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/28 上午 11:02
# @Author  : kamino

import os


class File(object):
    @staticmethod
    def write(path, data):
        with open(path, 'w', encoding='utf-8') as f:
            f.write(data)

    @staticmethod
    def add(path, data):
        with open(path, 'a', encoding='utf-8') as f:
            f.write(data)

    @staticmethod
    def read(path):
        if not os.path.exists(path):
            return None
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
