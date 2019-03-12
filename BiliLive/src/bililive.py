#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/8 下午 08:28
# @Author  : kamino

import os
import time
import subprocess
import threading
from .image import ImageCtrl


class BiliLive(object):
    def __init__(self, endtime, rtmpurl):
        """初始化"""
        self.ru = rtmpurl
        self.et = int(time.mktime(time.strptime(endtime, '%Y-%m-%d %H:%M:%S')))
        self.rp = os.path.abspath('.') + '/BiliLive/'
        self.st = int(time.time())

    def make_image(self, text=None, save=None):
        """生成帧"""
        if text == None:
            text = str(self.et - int(time.time()))
        text_flame = lambda x: ''.zfill(len(x))
        location = ((1280 - (len(text) * 200 * 0.5)) / 2, 250)
        size = 200
        ct = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        image = ImageCtrl.image_create(1280, 720)
        image = ImageCtrl.image_write(image, text_flame(text), location, size, (110, 0, 0, 50),
                                      self.rp + 'font/BONX-Silhouette.otf')
        image = ImageCtrl.image_write(image, text, location, size, (255, 117, 0, 0),
                                      self.rp + 'font/BONX-Medium.otf')
        image = ImageCtrl.image_write(image, text_flame(text), location, size, (0, 0, 0, 0),
                                      self.rp + 'font/BONX-Frame.otf')
        image = ImageCtrl.image_write(image, '距2020考研剩余', (100, 100), 60, (255, 117, 0, 0),
                                      self.rp + 'font/SetoFont-1.ttf')
        image = ImageCtrl.image_write(image, '秒', (1000, 530), 60, (255, 117, 0, 0),
                                      self.rp + 'font/SetoFont-1.ttf')
        image = ImageCtrl.image_write(image, 'SERVER TIME: %s' % ct, (500, 650), 20, (255, 117, 0, 0),
                                      self.rp + 'font/SetoFont-1.ttf')
        image = ImageCtrl.image_write(image, 'WWW.ISDUT.CN', (600, 690), 20, (255, 117, 0, 0),
                                      self.rp + 'font/SetoFont-1.ttf')
        if save != None:
            ImageCtrl.image_save(image, save)
        return ImageCtrl.image_tostring(image)

    def __make_thread(self):
        """生成图片线程"""
        print("MAKE THREAD START")
        sec = self.st + 5
        while True:
            if len(os.listdir(self.rp + 'temp')) >= 100:
                time.sleep(0.1)
                continue
            print("MAKE IMAGE -> %s" % sec)
            self.make_image(str(self.et - sec), '{rp}temp/{sec}.jpg'.format(rp=self.rp, sec=sec))
            sec += 1
            time.sleep(0.5)

    def __clean_thread(self):
        """清理缓存线程"""
        print("CLEAN THREAD START")
        while True:
            if len(os.listdir(self.rp + 'temp')) >= 100:
                for file in os.listdir(self.rp + 'temp'):
                    if int(file.replace('.jpg', '')) < int(time.time()):
                        os.remove(self.rp + 'temp/' + file)
                        print("CLEAN IMAGE -> %s" % file.replace('.jpg', ''))
            time.sleep(1)

    def __push_thread(self):
        """推流线程"""
        time.sleep(5)
        print("PUSH THREAD START")
        command = [
            'ffmpeg',
            '-y',
            '-f', 'rawvideo',
            '-vcodec', 'rawvideo',
            '-pix_fmt', 'bgr24',
            '-s', '1280x720',
            '-r', '23',
            '-i', '-',
            '-f', 'flv',
            self.ru
        ]
        pipe = subprocess.Popen(command, stdin=subprocess.PIPE)
        while True:
            ct = int(time.time())
            # print("PUSH IMAGE -> %s" % ct)
            if os.path.exists(self.rp + 'temp/%s.jpg' % ct):
                frame = ImageCtrl.image_read(self.rp + 'temp/%s.jpg' % ct)
                pipe.stdin.write(ImageCtrl.image_tostring(frame))
            else:
                print("IMAGE NOT FOUND {}".format(self.rp + 'temp/%s.jpg' % ct))

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
        command = [
            'ffmpeg',
            '-y',
            '-f', 'rawvideo',
            '-vcodec', 'rawvideo',
            '-pix_fmt', 'bgr24',
            '-s', '1280x720',
            '-r', '23',
            '-i', '-',
            '-f', 'flv',
            self.ru
        ]
        pipe = subprocess.Popen(command, stdin=subprocess.PIPE)

        while True:
            data = self.make_image()
            pipe.stdin.write(data)
        """
        threading.Thread(target=self.__make_thread).start()
        threading.Thread(target=self.__clean_thread).start()
        threading.Thread(target=self.__push_thread).start()
