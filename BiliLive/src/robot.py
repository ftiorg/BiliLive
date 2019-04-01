#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/26 下午 06:07
# @Author  : kamino

import time
import queue
from .config import Config
from .study import StudyExt
from .file import File
from .timer import Timer


class Robot(object):

    @staticmethod
    def text_msg(user_name, content):
        """处理文本消息"""
        content = content.replace('~喵', '')  # 愚人节
        File.add(Config.config('root-path') + 'BiliLive/save/danmu.log',
                 f'[{Timer.stamp2str(Timer.timestamp())}] {user_name}: {content}\n')
        if user_name == Config.config('auth')['name']:
            return None
        if content == "打卡":
            rank = StudyExt.SignAdd(user_name)
            if rank != None:
                return rank
            return '打卡失败，不知道为啥'

        return f'复读 {content}'

    @staticmethod
    def gift_msg(user_name, gift_name, gift_num):
        """处理礼物消息"""
        File.add(Config.config('root-path') + 'BiliLive/save/gift.log',
                 f'[{Timer.stamp2str(Timer.timestamp())}] {user_name}: {gift_name}x{gift_num}\n')
        if user_name == Config.config('auth')['username']:
            return None
        return f'感谢{user_name}的{gift_name}'
