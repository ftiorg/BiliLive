#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/14 下午 07:51
# @Author  : kamino

import os
from mutagen.mp3 import MP3


class AudioCtrl(object):
    @staticmethod
    def audio_info(file):
        if not os.path.exists(file):
            return None
        audio = MP3(file)
        return audio.info

    @staticmethod
    def audio_length(file):
        info = AudioCtrl.audio_info(file)
        return info.length or None
