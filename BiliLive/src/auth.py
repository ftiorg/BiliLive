#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/26 下午 09:54
# @Author  : kamino

import requests
import json
from .config import Config


class Auth(object):
    @staticmethod
    def get_cookie():
        """
        放弃使用,过不了csrf验证
        获取cookie的函数
        我这直接用的BilibiliHepler获取的cookie
        :return:
        requests的cookie
        """
        return None

    @staticmethod
    def get_data_by_uid(uid):
        """获取用户信息接口"""
        try:
            response = requests.post('http://space.bilibili.com/ajax/member/GetInfo', data={'mid': uid}, headers={
                'Referer': 'https://space.bilibili.com/%d/' % int(uid),
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
            })
            if response.status_code != 200:
                return None
            return json.loads(response.content)
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def get_uname(uid):
        """通过uid获取uname"""
        data = Auth.get_data_by_uid(uid)
        if data == None or data['status'] != True:
            return None
        return data['data']['name']
