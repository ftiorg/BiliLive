# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/16 下午 11:15
# @Author  : kamino

import os
import json
import requests
import random
import re
import time
import socket
from .database import DbLink
from .timer import Timer
from .auth import Auth
from .config import Config
from .error import Control


class Extension(object):
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
        Extension.E['user'][uid] = uname
        if int(Timer.stamp2str(Timer.timestamp(), '%H')) < 4:
            return '请在4点之后打卡,要注意休息哦'
        for k, s in enumerate(Extension.E['sign']):
            if uid in s:
                return f'{uname[0:2]}*已于{str(s[1])[0:5]}打卡成功,排名{k + 1}'
        dl = DbLink()
        Extension.E['sign'].append((uid, Timer.stamp2str(Timer.timestamp(), '%H:%M:%S')))
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
        if int(Timer.stamp2str(Timer.timestamp(), '%H')) < 4:
            Extension.E['sign'].clear()
            return ['请在4点之后打卡,要注意休息哦']
        if len(Extension.E['sign']) == 0:
            for sn in Extension.SignedList():
                Extension.E['sign'].append((sn[1], sn[4]))
        msg = []
        rank = Extension.E['sign']
        if len(rank) == 0:
            return ['暂无(可能会有1分钟延迟)']
        elif len(rank) < 5:
            max = len(rank)
        else:
            max = 5
        for i in range(max):
            try:
                uname = Extension.E['user'][rank[i][0]]
            except KeyError:
                Extension.E['user'][rank[i][0]] = Auth.get_uname(rank[i][0])
                uname = Extension.E['user'][rank[i][0]]
            msg.append(f'No{i + 1} {uname} {rank[i][1]}')
        return msg

    @staticmethod
    def IsSign(text=None):
        if re.search(r'打(.*)卡', text) == None and re.search(r'签(.*)到', text) == None:
            return False
        return True

    @staticmethod
    def ChgColor(text=None):
        """修改文字颜色"""
        r = re.search(r'color (.*)', text)
        if r == None:
            return False
        color = r.group(1)
        rgb = {
            'random': (999, 999, 999, 999),
            'reset': (255, 117, 0, 0),
            'red': (255, 0, 0, 0),
            'green': (0, 255, 0, 0),
            'blue': (0, 0, 0, 255)
        }
        try:
            Config.set('color', rgb[color])
            return True
        except KeyError:
            return False

    @staticmethod
    def ForbidBot(*args):
        """禁言机器人(分钟)"""
        Config.set('forbid', False)

    @staticmethod
    def AutoReboot(*args):
        """自动重启"""
        while True:
            time.sleep(60 * 60)
            print("AUTO RESTART AT %s" % Timer.stamp2str(Timer.timestamp(), '%H:%M:%S'))
            Control.force_exit()

    @staticmethod
    def MusicCtrlCore(arr):
        """
        与音乐服务器通信 TODO:整成异步的
        :param arr:
        :return:
        """
        try:
            if Config.get('bgmserver') == 'unix':
                sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                sock.settimeout(10)
                sock.connect(Config.get('unixpath'))
            else:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(10)
                sock.connect((Config.get('tcphost'), int(Config.get('tcpport'))))
            sock.send(json.dumps(arr).encode('utf-8'))
            recv = json.loads(sock.recv(10240).decode('utf-8'))
            if recv['data'] is False:
                raise Exception('执行失败')
            return recv['data']
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def MusicNext():
        """
        下一曲
        :return:
        """
        recv = Extension.MusicCtrlCore({"action": "next"})
        if recv is None:
            return '切歌失败'
        else:
            return '即将播放 %s' % recv['name']

    @staticmethod
    def MusicPlaying():
        """
        当前播放的啥
        :return:
        """
        recv = Extension.MusicCtrlCore({"action": "playing"})
        if recv is None:
            return '不知道呢'
        else:
            return '当前播放 %s' % recv['name']

    @staticmethod
    def MusicPlayingShow():
        """
        用于显示
        :return:
        """
        recv = Extension.MusicCtrlCore({"action": "playing"})
        if recv is None:
            return 'Unknown'
        else:
            return recv['name']

    @staticmethod
    def MusicWillplay():
        """
        下一曲是啥
        :return:
        """
        recv = Extension.MusicCtrlCore({"action": "playing"})
        if recv is None:
            return '不知道呢'
        else:
            return '下一首 %s' % recv['name']

    @staticmethod
    def IsAddMusic(text):
        """
        判断是否为点歌
        :param text:
        :return:
        """
        mat = re.search(r'点歌(.*)', text)
        if mat is None:
            return False
        if mat.group(0) == '':
            return 'https://music.163.com/#/song?id=156811'
        mid = mat.group(1).strip()
        try:
            int(mid)
            return 'https://music.163.com/#/song?id=%s' % mid
        except ValueError:
            return False

    @staticmethod
    def MusicAdd(url):
        """
        点歌
        :param url: 网易云音乐链接
        :return:
        """
        recv = Extension.MusicCtrlCore({"action": "add", "url": url})
        if recv is None:
            return '失败啦'
        else:
            return '成功 %s' % recv['name']
