#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/8 下午 08:59
# @Author  : kamino

import os
from .timer import Timer


class Error(Exception):
    def __init__(self, msg=None):
        print(msg)


class Control(object):
    @staticmethod
    def force_exit():
        """
        强行停止该进程
        :return:
        """
        print("EXIT AT %s" % Timer.stamp2str(Timer.timestamp()))
        os.system("ps -ef | grep bililive.py | grep -v grep | awk '{print $2}' | xargs --no-run-if-empty kill")
