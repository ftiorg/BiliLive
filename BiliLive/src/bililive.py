#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/8 下午 08:28
# @Author  : kamino

import os
import time
import subprocess
from .image import ImageCtrl


class BiliLive(object):
    def __init__(self, endtime, rtmpurl):
        """初始化"""
        self.ru = rtmpurl
        self.et = int(time.mktime(time.strptime(endtime, '%Y-%m-%d %H:%M:%S')))

    def make_image(self, text=None, save=False):
        """生成帧"""
        if text == None:
            text = str(self.et - int(time.time()))
        text_flame = lambda x: ''.zfill(len(x))
        location = ((1280 - (len(text) * 200 * 0.5)) / 2, 250)
        size = 200
        ct = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        image = ImageCtrl.image_create(1280, 720)
        image = ImageCtrl.image_write(image, text_flame(text), location, size, (110, 0, 0, 50),
                                      os.path.abspath('.') + '/BiliLive/font/BONX-Silhouette.otf')
        image = ImageCtrl.image_write(image, text, location, size, (255, 117, 0, 0),
                                      os.path.abspath('.') + '/BiliLive/font/BONX-Medium.otf')
        image = ImageCtrl.image_write(image, text_flame(text), location, size, (0, 0, 0, 0),
                                      os.path.abspath('.') + '/BiliLive/font/BONX-Frame.otf')
        image = ImageCtrl.image_write(image, '距2020考研剩余', (100, 100), 60, (255, 117, 0, 0),
                                      os.path.abspath('.') + '/BiliLive/font/SetoFont-1.ttf')
        image = ImageCtrl.image_write(image, '秒', (1000, 530), 60, (255, 117, 0, 0),
                                      os.path.abspath('.') + '/BiliLive/font/SetoFont-1.ttf')
        image = ImageCtrl.image_write(image, 'SERVER TIME: %s' % ct, (500, 650), 20, (255, 117, 0, 0),
                                      os.path.abspath('.') + '/BiliLive/font/SetoFont-1.ttf')
        image = ImageCtrl.image_write(image, 'WWW.ISDUT.CN', (600, 690), 20, (255, 117, 0, 0),
                                      os.path.abspath('.') + '/BiliLive/font/SetoFont-1.ttf')
        if save == True:
            ImageCtrl.image_save(image, os.path.abspath('.') + '/BiliLive/save/' + text + '.jpg')
        return ImageCtrl.image_tostring(image)

    def run(self):
        """运行"""
        """
        command2 = ['ffmpeg',
                    '-y',
                    '-f', 'rawvideo',
                    '-vcodec', 'rawvideo',
                    '-pix_fmt', 'bgr24',
                    '-s', '1280x720',
                    '-r', '25',
                    '-i', '-',
                    '-c:v', 'libx264',
                    '-pix_fmt', 'yuv420p',
                    '-preset', 'ultrafast',
                    '-f', 'flv',
                    self.ru]
        """
        command = [
            'ffmpeg',
            '-y',
            '-f', 'rawvideo',
            '-vcodec', 'rawvideo',
            '-pix_fmt', 'bgr24',
            '-s', '1280x720',
            '-r', '25',
            '-i', '-',
            '-f', 'flv',
            self.ru
        ]
        pipe = subprocess.Popen(command, stdin=subprocess.PIPE)

        while True:
            data = self.make_image()
            pipe.stdin.write(data)
