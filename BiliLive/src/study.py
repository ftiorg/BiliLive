#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/16 下午 11:15
# @Author  : kamino

import json
import requests
import random
from .database import DbLink
from .timer import Timer


class StudyExt(object):
    E = {'sign': []}

    @staticmethod
    def GetWord():
        """随机获取一个单词"""
        dl = DbLink()
        data = dl.query("SELECT * FROM `wordlist-2017` WHERE `ID` = '%d';" % random.randint(1, 5536))
        return data[0]

    @staticmethod
    def GetYiyan():
        """一言"""
        try:
            data = requests.get('https://v1.hitokoto.cn/', headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'}).content.decode()
            arr = json.loads(data)
            return (arr['hitokoto'], arr['from'])
        except Exception as e:
            return (str(e), 'ERROR')

    @staticmethod
    def SignedList():
        """每日签到"""
        dl = DbLink()
        data = dl.query(
            "SELECT * FROM `sign` WHERE `date` = '%s' ORDER BY 'time' ASC;" % Timer.stamp2str(Timer.timestamp(),
                                                                                              '%Y-%m-%d'))
        return data

    @staticmethod
    def SignAdd(name=None):
        """添加签到"""
        if name == None:
            return False
        if int(Timer.stamp2str(Timer.timestamp(), '%H')) <= 4:
            return False
        StudyExt.E['sign'].append((name, Timer.stamp2str(Timer.timestamp(), '%H:%M:%S')))
        dl = DbLink()
        dl.insert("INSERT INTO `sign`(`uid`, `name`, `date`, `time`) VALUES ('%s', '%s', '%s', '%s');" % (
            name, name, Timer.stamp2str(Timer.timestamp(),
                                        '%Y-%m-%d'), Timer.stamp2str(Timer.timestamp(),
                                                                     '%H:%M:%S')))
        return dl.query(
            "SELECT COUNT(*) FROM `sign` WHERE `date` = '%s' ORDER BY 'time' ASC;" % Timer.stamp2str(Timer.timestamp(),
                                                                                                     '%Y-%m-%d'))[0][0]

    @staticmethod
    def SignRank():
        """签到排名"""
        if int(Timer.stamp2str(Timer.timestamp(), '%H')) <= -1:
            return '请在4点之后打卡,要注意休息哦'
        msg = ''
        rank = StudyExt.E['sign']
        if len(rank) == 0:
            return '暂无'
        elif len(rank) < 1:
            max = len(rank)
        else:
            max = 1
        for i in range(max):
            msg += f'No{i + 1} {rank[i][0]} {rank[i][1]}'
        return msg
