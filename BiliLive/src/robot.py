#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/26 下午 06:07
# @Author  : kamino

import time
import queue
from .config import Config
from .study import StudyExt


class Robot(object):

    @staticmethod
    def text_msg(user_name, content):
        """处理文本消息"""
        if user_name == Config.config('auth')['username']:
            return None
        if content == "打卡":
            rank = StudyExt.SignAdd(user_name)
            return f'{user_name}打卡成功,今日排名{rank}'

        return f'复读 {content}'

    @staticmethod
    def gift_msg(user_name, gift_name, gift_num):
        """处理礼物消息"""
        if user_name == Config.config('auth')['username']:
            return None
        return f'感谢{user_name}的{gift_name}'
