#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/26 下午 04:02
# @Author  : kamino

import asyncio
import threading
import requests
from .blivedm.blivedm import BLiveClient
from .config import Config
from .timer import Timer
from .robot import Robot


class MyBLiveClient(BLiveClient):
    # 演示如何自定义handler
    _COMMAND_HANDLERS = BLiveClient._COMMAND_HANDLERS.copy()
    _COMMAND_HANDLERS['SEND_GIFT'] = lambda client, command: client._my_on_gift(
        command['data']['giftName'], command['data']['num'], command['data']['uname'],
        command['data']['coin_type'], command['data']['total_coin']
    )

    async def _on_get_danmaku(self, content, user_name):
        print(f'{user_name}：{content}')
        DanmuHandle.send(Robot.text_msg(user_name, content))

    async def _my_on_gift(self, gift_name, gift_num, user_name, coin_type, total_coin):
        print(f'{user_name} 赠送{gift_name}x{gift_num} （{coin_type}币x{total_coin}）')
        DanmuHandle.send(Robot.gift_msg(user_name, gift_name, gift_num))


class DanmuHandle(object):
    @staticmethod
    async def async_main():
        client = MyBLiveClient(Config.config('room-id'), True)
        future = client.run()
        try:
            await future
        finally:
            await client.close()

    @staticmethod
    def run(loop):
        try:
            # loop = asyncio.get_event_loop()
            loop.run_until_complete(DanmuHandle.async_main())
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def send(msg=None):
        """发送消息"""
        if msg == None:
            return False
        try:
            data = {
                "color": 16777215,
                "fontsize": 25,
                "mode": "1",
                "msg": msg,
                "rnd": Timer.timestamp(),
                "roomid": Config.config('room-id'),
                "bubble": 0,
                "csrf_token": Config.config('csrf'),
                "csrf": Config.config('auth')['csrf']
            }
            headers = {
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Origin": "https://live.bilibili.com",
                "Referer": "https://live.bilibili.com/%d" % Config.config('room-id'),
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
                "Cookie": Config.config('auth')['cookie']
            }
            response = requests.post('https://api.live.bilibili.com/msg/send', data=data, headers=headers)
            print('SEND MSG:%s(%s)' % (msg, response.content.decode()))
        except Exception as e:
            print(e)
            return False
