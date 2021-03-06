#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/26 下午 06:07
# @Author  : kamino

import os
import re
import linecache
import random
from .config import Config
from .extension import Extension
from .file import File
from .timer import Timer
from .error import Control


class Robot(object):

    @staticmethod
    def text_msg(user_id, user_name, content):
        """处理文本消息"""
        File.add(Config.get('root-path') + 'BiliLive/save/danmu.log',
                 f'[{Timer.stamp2str(Timer.timestamp())}] {user_id}({user_name}): {content}\n')
        if user_name == Config.get('auth')['name']:
            return None
        if Extension.IsSign(content):
            rank = Extension.SignAdd(user_id, user_name)
            if rank != None:
                return rank
            return '打卡失败，不知道为啥'
        if content == 'sudo reboot':
            print("SUDO RESTART")
            Control.force_exit()
        if Extension.ChgColor(content):
            return '喵'
        if content == '禁言小弟':
            Config.set('forbid', True)
            Timer.timer_add(action=Extension.ForbidBot, runat=Timer.timestamp() + (5 * 60))
            return None
        if content == '解除禁言':
            Config.set('forbid', False)
            return '喵'
        if content == '切歌' or content == '下一首':
            return Extension.MusicNext()
        if content == '下一首是啥':
            return Extension.MusicWillplay()
        if Extension.IsAddMusic(content) is not False:
            return Extension.MusicAdd(Extension.IsAddMusic(content))
        if content == 'hello kamino':
            return Extension.HelloKamino(user_id)
        if Extension.HasKey(content, '天'):
            return Extension.FuxiDays()

        return RobotReply.reply(user_id, user_name, content)

    @staticmethod
    def gift_msg(user_id, user_name, gift_name, gift_num):
        """处理礼物消息"""
        File.add(Config.get('root-path') + 'BiliLive/save/gift.log',
                 f'[{Timer.stamp2str(Timer.timestamp())}] {user_id}({user_name}): {gift_name}x{gift_num}\n')
        return f'感谢{user_name}的{gift_num}个{gift_name}喵~'


class RobotReply(object):

    @staticmethod
    def reply(user_id=0, user_name=0, content=''):
        """处理消息"""
        message = linecache.getline(Config.get('root-path') + 'BiliLive/save/subtitle_wuyu.txt',
                                    random.randint(1, 30910)).replace('\n', '')

        return re.sub(r'[\u4e00-\u9fa5]', '喵', message)[:30]
