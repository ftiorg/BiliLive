#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/8 下午 07:08
# @Author  : kamino

"""
librtmp安装失败，这里用ffmpeg进行推流
"""

import os
import time

class rtmp(object):
    def __init__(self,url):
        """初始化设置推流地址"""
        self.url = url