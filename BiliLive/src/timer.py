#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/26 下午 10:41
# @Author  : kamino

import time
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
    def str2stamp(s, f='%Y-%m-%d %H:%M:%S'):
        """时间字符串转时间戳"""
        return int(time.mktime(time.strptime(s, f)))

    @staticmethod
    def stamp2str(t, f='%Y-%m-%d %H:%M:%S'):
        """时间戳转时间字符串"""
        return time.strftime(f, time.localtime(t))

    @staticmethod
    def timer():
        """定时器"""
        while True:
            works_temp = Timer.WORKS.copy()
            for wid, item in works_temp.items():
                if Timer.timestamp() >= item['runat']:
                    # TODO: 使用异步
                    """
                    loop = asyncio.get_event_loop()
                    loop.run_until_complete(Timer.timer_run(id))
                    loop.close()
                    """
                    if not (item['finish'] or item['running']):
                        threading.Thread(target=Timer.timer_run, args=(wid,)).start()
                        Timer.WORKS[wid]['running'] = True

    @staticmethod
    def timer_add(action, runat, arg=()):
        """
        添加定时器
        :param action: 调用函数
        :param runat: 启动时间
        :param arg: 参数
        :return: int 定时器ID
        """
        wid = Encrypt.md5(str(action))[:5] + Encrypt.key(5)
        Timer.WORKS[wid] = {
            'wid': wid,
            'action': action,
            'args': arg,
            'runat': runat,
            'running': False,
            'finish': False
        }
        print(f'ADD WORK {wid} AT {runat}')
        return wid

    @staticmethod
    def timer_remove(wid):
        """
        删除定时器
        :param wid: 定时器ID
        :return: bool
        """
        del Timer.WORKS[wid]
        print(f'REMOVE WORK {wid}')

    @staticmethod
    def timer_running(wid):
        """
        设置为正在运行
        :param wid:
        :return:
        """
        Timer.WORKS[wid]['running'] = True

    @staticmethod
    def timer_run(wid):
        """
        执行一个定时器任务
        :param wid:
        :return:
        """
        print(f'RUN WORK {wid}')
        try:
            Timer.WORKS[wid]['action'](Timer.WORKS[wid]['args'])
            print(f'WORK {wid} FINISH')
        except Exception as e:
            print(f'WORK {wid} ERROR {str(e)}')
        finally:
            Timer.timer_remove(wid)
