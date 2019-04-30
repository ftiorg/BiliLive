#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/26 下午 10:41
# @Author  : kamino

import time
import asyncio
import random
import threading
from .encrypt import Encrypt


class Timer(object):
    WORKS = {}

    @staticmethod
    def timestamp():
        """返回13位时间戳"""
        return int(time.time())

    @staticmethod
    def timestamp_str():
        """返回str时间戳"""
        return str(int(time.time()))

    @staticmethod
    def str2stamp(s, format='%Y-%m-%d %H:%M:%S'):
        """时间字符串转时间戳"""
        return int(time.mktime(time.strptime(s, format)))

    @staticmethod
    def stamp2str(t, format='%Y-%m-%d %H:%M:%S'):
        """时间戳转时间字符串"""
        return time.strftime(format, time.localtime(t))

    @staticmethod
    def timer():
        """定时器"""
        while True:
            for id, item in Timer.WORKS.items():
                if Timer.timestamp() >= item['runat'] and item['finish'] == False:
                    """
                    loop = asyncio.get_event_loop()
                    loop.run_until_complete(Timer.timer_run(id))
                    loop.close()
                    """
                    threading.Thread(target=Timer.timer_run(id)).start()

    @staticmethod
    def timer_add(action, runat, args=None):
        """
        添加定时器
        :param action: 调用函数
        :param runat: 启动时间
        :return: int 定时器ID
        """
        id = Encrypt.md5(str(action))[:5] + Encrypt.md5(str(random.randint(0, 9999)))[:5]
        Timer.WORKS[id] = {'action': action, 'args': args, 'runat': runat, 'repeat': False, 'finish': False}
        print(f'ADD WORK {id} AT {runat}')
        return id

    @staticmethod
    def timer_remove(id):
        """
        删除定时器
        :param id: 定时器ID
        :return: bool
        """
        # del Timer.WORKS[id]
        Timer.WORKS[id]['finish'] = True
        print(f'REMOVE WORK {id}')

    @staticmethod
    def timer_run(id):
        """
        执行一个定时器任务
        :param id:
        :param args:
        :return:
        """
        print(f'RUN WORK {id}')
        try:
            Timer.WORKS[id]['action']()
            Timer.timer_remove(id)
            print(f'WORK {id} FINISH')
        except Exception as e:
            print(f'WORK {id} ERROR {str(e)}')
