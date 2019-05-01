#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/30 下午 11:54
# @Author  : kamino

import hashlib
import random
import base64
import binascii
import pymysql
from Crypto.Cipher import AES


class Encrypt(object):

    @staticmethod
    def md5(text=''):
        """计算md5"""
        return hashlib.md5(text.encode('utf-8')).hexdigest()

    @staticmethod
    def sha1(text=''):
        """计算sha1"""
        return hashlib.sha1(text.encode('utf-8')).hexdigest()

    @staticmethod
    def key(len=16):
        """生成指定位数字符串"""
        di = '0123456789abcdef'
        key = ''
        for i in range(len):
            key += di[random.randint(0, 15)]
        return key

    @staticmethod
    def fill_to_16x(text=''):
        """补全到16x位"""
        fill = lambda x: ('\0' * x)
        return text + fill(len(str(text)) // 16 + 1 * 16 - len(str(text)) % 16)

    @staticmethod
    def aes_encrypt(text='', key='0000000000000000'):  # TODO 不支持中文！
        """AES加密"""
        aes = AES.new(Encrypt.fill_to_16x(key).encode('utf-8'), AES.MODE_ECB)
        return binascii.b2a_hex(aes.encrypt(Encrypt.fill_to_16x(text).encode('utf-8'))).decode('utf-8')

    @staticmethod
    def aes_decrypt(text='', key='0000000000000000'):  # TODO 不支持中文！
        """AES解密"""
        aes = AES.new(Encrypt.fill_to_16x(key).encode('utf-8'), AES.MODE_ECB)
        return aes.decrypt(binascii.a2b_hex(text)).decode('utf-8').replace('\0', '')

    @staticmethod
    def trans_str(s=None):
        """转义字符串"""
        return pymysql.escape_string(s)
