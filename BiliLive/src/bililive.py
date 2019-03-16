#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/8 下午 08:28
# @Author  : kamino

import os
import time
import subprocess
import threading
import json
from .image import ImageCtrl
from .audio import AudioCtrl


class BiliLive(object):
    def __init__(self, endtime=None, rtmpurl=None):
        """初始化"""
        self.ru = rtmpurl  # 推流地址
        self.et = endtime and int(time.mktime(time.strptime(endtime, '%Y-%m-%d %H:%M:%S')))  # 结束时间
        self.rp = os.path.abspath('.') + '/BiliLive/'  # BiliLive目录
        self.st = int(time.time())  # 开始时间
        self.ef = False  # 错误标识符
        self.cf = {}  # 配置项
        self.bn = ''  # 背景音乐
        self.nl = open(os.devnull, 'w')  # 虚空
        if not os.path.exists(self.rp + 'temp'):
            os.mkdir(self.rp + 'temp', 777)
            print("CREATE DIR -> TEMP")
        if not os.path.exists(self.rp + 'save'):
            os.mkdir(self.rp + 'save', 777)
            print("CREATE DIR -> SAVE")

    def config(self, config=None):
        """设置配置文件"""
        if os.path.exists(config):
            print("LOAD CONFIG FROM %s" % config)
            with open(config, 'r') as c:
                for key, value in json.loads(c.read()).items():
                    self.cf[key] = value
                    print("SET %s AS %s" % (key, value))
                self.ru = self.cf['rtmp-url']
                self.et = int(time.mktime(time.strptime(self.cf['end-time'], '%Y-%m-%d %H:%M:%S')))
        else:
            print("FILE NOT FOUND %s" % config)

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
        image = ImageCtrl.image_write(image, 'BGM: stars in the rain - Aimer', (20, 680), 20, (255, 117, 0, 0),
                                      self.rp + 'font/SetoFont-1.ttf')
        if save != None:
            ImageCtrl.image_save(image, save)
        return ImageCtrl.image_tostring(image)

    def _make_thread(self):
        """生成图片线程"""
        print("MAKE THREAD START")
        sec = self.st + 2
        while not self.ef:
            if len(os.listdir(self.rp + 'temp')) >= 200:
                time.sleep(0.1)
                continue
            print("MAKE IMAGE -> %s" % sec)
            with open('{rp}temp/{sec}.jpgx'.format(rp=self.rp, sec=sec), 'wb') as image:
                image.write(self.make_image(str(self.et - sec)))
            sec += 1
            time.sleep(0.1)
        print("MAKE THREAD EXIT")

    def _clean_thread(self):
        """清理缓存线程"""
        print("CLEAN THREAD START")
        while not self.ef:
            if len(os.listdir(self.rp + 'temp')) >= 150:
                for file in os.listdir(self.rp + 'temp'):
                    if int(file.replace('.jpgx', '')) < int(time.time()) - 10:
                        os.remove(self.rp + 'temp/' + file)
                        print("CLEAN IMAGE -> %s" % file.replace('.jpgx', ''))
            time.sleep(1)
        print("CLEAN THREAD EXIT")

    def _push_thread(self):
        """推流线程"""
        time.sleep(2)
        print("PUSH THREAD START")
        command = [
            'ffmpeg',
            '-y',
            '-f', 'rawvideo',
            '-vcodec', 'rawvideo',
            '-pix_fmt', 'bgr24',
            '-s', '1280x720',
            '-re',
            '-i', '-',
            '-i', 'rtmp://127.0.0.1:1935/rtmp/music',
            '-f', 'flv',
            '-b:v', '1k',
            self.ru
        ]
        pipe = subprocess.Popen(command, stdin=subprocess.PIPE)

        while True:
            ct = int(time.time())
            if os.path.exists(self.rp + 'temp/%s.jpgx' % ct):
                with open(self.rp + 'temp/%s.jpgx' % ct, 'rb') as image:
                    try:
                        pipe.stdin.write(image.read())
                    except BrokenPipeError as e:
                        self.ef = True
                        print(e)
                        break
                    except KeyboardInterrupt as e:
                        self.ef = True
                        print(e)
                        break
            else:
                print("IMAGE NOT FOUND {}".format(self.rp + 'temp/%s.jpgx' % ct))
        print("PUSH THREAD EXIT")

    def _clean_temp(self):
        """删除所有缓存"""
        for file in os.listdir(self.rp + 'temp'):
            os.remove(self.rp + 'temp/' + file)
            print("CLEAN IMAGE -> %s" % file.replace('.jpgx', ''))

    def _bgm_thread(self):
        """背景音乐线程"""
        print("MUSIC THREAD START")
        while not self.ef:
            for music in self.cf['bgm-list']:
                try:
                    command = [
                        'ffmpeg',
                        '-y',
                        '-i', music,
                        '-f', 'flv',
                        'rtmp://127.0.0.1:1935/rtmp/music'
                    ]
                    up = subprocess.call(command, shell=False, stdout=self.nl)
                except Exception as e:
                    print(e)
            time.sleep(1)
        print("MUSIC THREAD EXIT")

    def __del__(self):
        """退出时清理"""
        self._clean_temp()

    def test(self):
        """
        image = self.make_image(str(self.et - int(time.time())))
        ImageCtrl.image_show(ImageCtrl.image_fromstring(image))
        """
        print(AudioCtrl.audio_info(self.rp + 'save/bgm.mp3').length)

    def run(self):
        """运行"""
        threading.Thread(target=self._make_thread).start()
        threading.Thread(target=self._clean_thread).start()
        threading.Thread(target=self._bgm_thread).start()
        threading.Thread(target=self._push_thread).start()
