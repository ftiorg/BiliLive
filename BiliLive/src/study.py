#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/16 下午 11:15
# @Author  : kamino

import json
import requests
import random
import re
from .database import DbLink
from .timer import Timer
from .auth import Auth


class StudyExt(object):
    E = {'sign': [], 'user': {}}

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
        """已签到列表"""
        dl = DbLink()
        data = dl.query(
            "SELECT * FROM `sign` WHERE `date` = '%s' ORDER BY 'time' ASC;" % Timer.stamp2str(Timer.timestamp(),
                                                                                              '%Y-%m-%d'))
        return data

    @staticmethod
    def SignAdd(uid, uname):
        """添加签到"""
        StudyExt.E['user'][uid] = uname
        if int(Timer.stamp2str(Timer.timestamp(), '%H')) <= 4:
            return '请在4点之后打卡,要注意休息哦'
        for k, s in enumerate(StudyExt.E['sign']):
            if uid in s:
                return f'{uname[0:2]}*已于{str(s[1])[0:5]}打卡成功,排名{k + 1}'
        dl = DbLink()
        StudyExt.E['sign'].append((uid, Timer.stamp2str(Timer.timestamp(), '%H:%M:%S')))
        dl.insert("INSERT INTO `sign`(`uid`, `name`, `date`, `time`) VALUES ('%s', '%s', '%s', '%s');" % (
            uid, uname, Timer.stamp2str(Timer.timestamp(),
                                        '%Y-%m-%d'), Timer.stamp2str(Timer.timestamp(),
                                                                     '%H:%M:%S')))
        rk = dl.query(
            "SELECT COUNT(*) FROM `sign` WHERE `date` = '%s' ORDER BY 'time' ASC;" % Timer.stamp2str(Timer.timestamp(),
                                                                                                     '%Y-%m-%d'))[0][0]
        return f'{uname[0:2]}*打卡成功,今日排名{rk}'

    @staticmethod
    def SignRank():
        """签到排名"""
        if int(Timer.stamp2str(Timer.timestamp(), '%H')) <= 4:
            StudyExt.E['sign'].clear()
            return ['请在4点之后打卡,要注意休息哦']
        if len(StudyExt.E['sign']) == 0:
            for sn in StudyExt.SignedList():
                StudyExt.E['sign'].append((sn[1], sn[4]))
        msg = []
        rank = StudyExt.E['sign']
        if len(rank) == 0:
            return ['暂无(可能会有1分钟延迟)']
        elif len(rank) < 5:
            max = len(rank)
        else:
            max = 5
        for i in range(max):
            try:
                uname = StudyExt.E['user'][rank[i][0]]
            except KeyError:
                StudyExt.E['user'][rank[i][0]] = Auth.get_uname(rank[i][0])
                uname = StudyExt.E['user'][rank[i][0]]
            msg.append(f'No{i + 1} {uname} {rank[i][1]}')
        return msg

    @staticmethod
    def IsSign(text=None):
        if re.search(r'打(.*)卡',text) == None:
            return False
        return True
