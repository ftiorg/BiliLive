#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/14 下午 07:51
# @Author  : kamino

import os

from mutagen.mp3 import MP3
from .config import Config


class AudioCtrl(object):
    """ only support mp3 now! """
    MUSIC_LIST = []
    MUSIC_DIR = None

    @staticmethod
    def audio_list():
        """
        获取BGM列表
        :return:
        """
        if AudioCtrl.MUSIC_DIR is None:
            AudioCtrl.MUSIC_DIR = Config.get('root-path') + 'BiliLive/music/'

        li = []

        for item in os.listdir(AudioCtrl.MUSIC_DIR):
            if item.endswith('.mp3'):
                path = os.path.abspath(AudioCtrl.MUSIC_DIR + item)
                info = AudioCtrl.audio_info(path)
                if info is None:
                    continue
                li.append({
                    'name': item,
                    'path': path,
                    'length': info.length
                })
        return li

    @staticmethod
    def audio_info(file):
        """
        获取音频信息
        :param file:
        :return:
        """
        try:
            audio = MP3(file)
            return audio.info
        except Exception:
            return None

    @staticmethod
    def audio_length(file):
        info = AudioCtrl.audio_info(file)
        return info.length or None

    @staticmethod
    def audio_title(file):
        info = AudioCtrl.audio_info(file)
        return info.length or None
