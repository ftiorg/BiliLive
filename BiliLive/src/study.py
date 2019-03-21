#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/16 下午 11:15
# @Author  : kamino

import json
import requests
import random
from .database import DbLink


class StudyExt(object):

    @staticmethod
    def GetWord():
        """随机获取一个单词"""
        dl = DbLink()
        data = dl.execute("SELECT * FROM `wordlist-2017` WHERE `ID` = '%d';" % random.randint(1, 5536))
        return data

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
