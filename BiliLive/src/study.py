#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/16 下午 11:15
# @Author  : kamino

import random
from .database import DbLink


class StudyExt(object):

    @staticmethod
    def GetWord():
        """随机获取一个单词"""
        dl = DbLink()
        data = dl.execute("SELECT * FROM `wordlist-2017` WHERE `ID` = '%d';" % random.randint(1, 5536))
        return data
