#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/26 下午 04:02
# @Author  : kamino

import requests
import time
from .blivedm.blivedm import BLiveClient
from .config import Config
from .timer import Timer
from .robot import Robot
from .database import DbLink
from .encrypt import Encrypt

"""
danmu = {'cmd': 'DANMU_MSG', 'info': [[0, 1, 25, 16777215, 1556697136, 1556696728, 0, 'a8442e3f', 0, 0, 0], 'hello',
                                      [61730039, 'kamino大佬的小弟', 1, 0, 0, 10000, 1, ''],
                                      [4, '米鹿', '姬野米鹿', 3556018, 6406234, ''], [24, 0, 5805790, '>50000'], ['', ''], 0,
                                      0, None, {'ts': 1556697136, 'ct': '2D417F59'}]}

gift = {'cmd': 'SEND_GIFT', 'data': {'giftName': '辣条', 'num': 5, 'uname': 'kamino大佬的小弟',
                                     'face': 'http://i1.hdslb.com/bfs/face/733d408fc42b5ed6a254c2b6cd9429f7f1eca2f5.jpg',
                                     'guard_level': 0, 'rcost': 32978, 'uid': 61730039, 'top_list': [],
                                     'timestamp': 1556697158, 'giftId': 1, 'giftType': 0, 'action': '喂食', 'super': 0,
                                     'super_gift_num': 0, 'price': 100, 'rnd': '1556696728', 'newMedal': 0,
                                     'newTitle': 0, 'medal': [], 'title': '', 'beatId': '0', 'biz_source': 'live',
                                     'metadata': '', 'remain': 13, 'gold': 0, 'silver': 0, 'eventScore': 0,
                                     'eventNum': 0, 'smalltv_msg': [], 'specialGift': None, 'notice_msg': [],
                                     'capsule': None, 'addFollow': 0, 'effect_block': 1, 'coin_type': 'silver',
                                     'total_coin': 500, 'effect': 0, 'tag_image': '', 'user_count': 0}}

"""


class MyBLiveClient(BLiveClient):
    _COMMAND_HANDLERS = BLiveClient._COMMAND_HANDLERS.copy()
    _COMMAND_HANDLERS['DANMU_MSG'] = lambda client, command: client._my_on_get_danmaku(
        command['info'][2][0], command['info'][2][1], command['info'][1]
    )
    _COMMAND_HANDLERS['SEND_GIFT'] = lambda client, command: client._my_on_gift(
        command['data']['uid'],
        command['data']['uname'],
        command['data']['giftName'],
        command['data']['num'],
        command['data']['coin_type'],
        command['data']['total_coin']
    )

    async def _my_on_get_danmaku(self, user_id, user_name, content):
        print(f'{user_name}：{content}')
        DanmuSave.danmu(user_id, user_name, content)
        DanmuHandle.send(Robot.text_msg(user_id, user_name, content))

    async def _my_on_gift(self, user_id, user_name, gift_name, gift_num, coin_type, total_coin):
        print(f'{user_name} 赠送{gift_name}x{gift_num} ({coin_type}币x{total_coin})')
        DanmuSave.gift(user_id, user_name, gift_name, gift_num)
        DanmuHandle.send(Robot.gift_msg(user_id, user_name, gift_name, gift_num))


class DanmuHandle(object):
    @staticmethod
    async def async_main():
        client = MyBLiveClient(Config.get('room-id'), False)
        future = client.run()
        try:
            await future
        except Exception as e:
            DanmuHandle.send(str(e))
            time.sleep(5)
            await DanmuHandle.async_main()
        finally:
            await client.close()

    @staticmethod
    def run(loop):
        try:
            loop.run_until_complete(DanmuHandle.async_main())
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def send(msg=None):
        """发送消息"""
        if msg is None or Config.get('forbid'):
            return False
        try:
            data = {
                "color": 16777215,
                "fontsize": 25,
                "mode": "1",
                "msg": msg[0:30],
                "rnd": Timer.timestamp(),
                "roomid": Config.get('room-id'),
                "bubble": 0,
                "csrf_token": Config.get('csrf'),
                "csrf": Config.get('auth')['csrf']
            }
            headers = {
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Origin": "https://live.bilibili.com",
                "Referer": "https://live.bilibili.com/%d" % Config.get('room-id'),
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
                "Cookie": Config.get('auth')['cookie']
            }
            response = requests.post('https://api.live.bilibili.com/msg/send', data=data, headers=headers)
            print('SEND MSG:%s(%s)' % (msg, response.content.decode()))
        except Exception as e:
            print(e)
            return False


class DanmuSave(object):
    DB = None

    @staticmethod
    def connect():
        """链接到数据库"""
        DanmuSave.DB = DbLink()

    @staticmethod
    def danmu(user_id, user_name, content):
        """保存弹幕消息"""
        if DanmuSave.DB is None:
            DanmuSave.connect()
        DanmuSave.DB.insert(
            "INSERT INTO `danmu`(`uid`, `name`, `msg`, `time`) VALUES ('%s','%s','%s','%s');" % (
                user_id, user_name, Encrypt.trans_str(content), Timer.stamp2str(Timer.timestamp())))

    @staticmethod
    def gift(user_id, user_name, gift_name, gift_num):
        """保存礼物消息"""
        if DanmuSave.DB is None:
            DanmuSave.connect()
        DanmuSave.DB.insert(
            "INSERT INTO `gift`(`uid`, `name`, `gift`, `num`, `time`) VALUES ('%s','%s','%s','%s','%s');" % (
                user_id, user_name, gift_name, gift_num, Timer.stamp2str(Timer.timestamp())))
