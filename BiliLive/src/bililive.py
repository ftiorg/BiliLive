#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/8 下午 08:28
# @Author  : kamino

import os
import time
import subprocess
import threading
import asyncio
import random
from .image import ImageCtrl
from .audio import AudioCtrl
from .extension import Extension
from .danmu import DanmuHandle
from .config import Config
from .timer import Timer
from .error import Control


class BiliLive(object):

    def __init__(self):
        """
        初始化
        """
        self.ru = Config.get('rtmp-url')  # 推流地址
        self.et = Timer.str2stamp(Config.get('end-time'))  # 结束时间
        self.rp = Config.get('root-path') + 'BiliLive/'  # BiliLive目录
        self.st = Timer.timestamp()  # 开始时间
        self.ef = False  # 错误标识符
        self.cf = Config.get()  # 配置项
        self.bn = None  # 背景音乐
        self.wd = Extension.GetWord()  # 加个单词
        self.yy = Extension.GetYiyan()  # 一言API
        if not os.path.exists(self.rp + 'temp'):
            os.mkdir(self.rp + 'temp', 777)
            print("CREATE DIR -> TEMP")
        if not os.path.exists(self.rp + 'save'):
            os.mkdir(self.rp + 'save', 777)
            print("CREATE DIR -> SAVE")

    def config_init(self):
        """
        初始化配置项
        :return:
        """
        Config.set('color', (255, 117, 0, 0))
        Config.set('forbid', False)
        # Config.set('addimage', ImageCtrl.image_read(self.rp + 'image/goldfish.png'))

    def make_image(self, text=None, save=None, show=False):
        """
        生成帧
        :param text:
        :param save:
        :param show:
        :return:
        """
        if text == None:
            text = str(self.et - Timer.timestamp())
        text_flame = lambda x: ''.zfill(len(x))
        location = ((1280 - (len(text) * 200 * 0.5)) / 2, 250)
        size = 200
        if Config.get('color') == (999, 999, 999, 999):
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 0)
        else:
            color = Config.get('color')
        ct = Timer.stamp2str(time.time())
        image = ImageCtrl.image_create(1280, 720)
        image = ImageCtrl.image_write(image, '距2020考研剩余', (100, 100), 60, color,
                                      self.rp + 'font/SetoFont-1.ttf')
        image = ImageCtrl.image_write(image, text_flame(text), location, size, (110, 0, 0, 50),
                                      self.rp + 'font/BONX-Silhouette.otf')
        image = ImageCtrl.image_write(image, text, location, size, color,
                                      self.rp + 'font/BONX-Medium.otf')
        image = ImageCtrl.image_write(image, text_flame(text), location, size, (0, 0, 0, 0),
                                      self.rp + 'font/BONX-Frame.otf')
        image = ImageCtrl.image_write(image, '秒', (1100, 300), 60, color,
                                      self.rp + 'font/SetoFont-1.ttf')
        image = ImageCtrl.image_write(image, '%d天' % (int(text) / 86400 + 1), (530, 500), 60,
                                      color,
                                      self.rp + 'font/SetoFont-1.ttf')
        image = ImageCtrl.image_write(image, self.wd[1], (20, 550), 40, color,
                                      self.rp + 'font/SourceHanSansCN-Medium.otf')
        image = ImageCtrl.image_write(image, self.wd[2], (20, 600), 30, color,
                                      self.rp + 'font/SourceHanSansCN-Medium.otf')
        image = ImageCtrl.image_write(image, self.yy[0] + ' —— ' + self.yy[1], (5, 5), 20, color,
                                      self.rp + 'font/SourceHanSansCN-Medium.otf')
        image = ImageCtrl.image_write(image, 'SERVER TIME: %s' % ct, (500, 650), 20, color,
                                      self.rp + 'font/SetoFont-1.ttf')
        image = ImageCtrl.image_write(image, 'WWW.ISDUT.CN', (600, 690), 20, color,
                                      self.rp + 'font/SetoFont-1.ttf')
        image = ImageCtrl.image_write(image, 'BGM: %s' % Extension.MusicPlayingShow(), (20, 680), 20, color,
                                      self.rp + 'font/SourceHanSansCN-Medium.otf')
        image = ImageCtrl.image_write(image, '早起打卡前五名', (800, 100), 25, color,
                                      self.rp + 'font/SourceHanSansCN-Medium.otf')
        # image = ImageCtrl.image_cover(image, Config.get('addimage'), (875, 492))
        for key, rk in enumerate(Extension.SignRank()):
            image = ImageCtrl.image_write(image, rk, (800, key * 24 + 125), 20, color,
                                          self.rp + 'font/SourceHanSansCN-Medium.otf')
        if save != None:
            ImageCtrl.image_save(image, save)
        if show:
            ImageCtrl.image_show(image)
        return ImageCtrl.image_tostring(image)

    def _make_thread(self):
        """
        生成图片线程
        :return: 
        """
        print("MAKE THREAD START")
        sec = self.st + 2
        count_wd = 0
        count_yy = 0
        while not self.ef:
            if len(os.listdir(self.rp + 'temp')) >= 10:
                time.sleep(0.1)
                continue
            if count_wd == 5:
                self.wd = Extension.GetWord()
                count_wd = 0
            if count_yy == 12:
                self.yy = Extension.GetYiyan()
                count_yy = 0

            print("MAKE IMAGE -> %s" % sec)
            with open('{rp}temp/{sec}.jpgx'.format(rp=self.rp, sec=sec), 'wb') as image:
                image.write(self.make_image(str(self.et - sec)))
            sec += 1
            count_wd += 1
            count_yy += 1
            time.sleep(0.01)
        print("MAKE THREAD EXIT")

    def _clean_thread(self):
        """
        清理缓存线程
        :return:
        """
        print("CLEAN THREAD START")
        while not self.ef:
            if len(os.listdir(self.rp + 'temp')) >= 5:
                for file in os.listdir(self.rp + 'temp'):
                    if int(file.replace('.jpgx', '')) < Timer.timestamp() - 2:
                        os.remove(self.rp + 'temp/' + file)
                        print("CLEAN IMAGE -> %s" % file.replace('.jpgx', ''))
            time.sleep(1)
        print("CLEAN THREAD EXIT")

    def _push_thread(self):
        """
        推流线程
        :return:
        """
        time.sleep(2)
        print("PUSH THREAD START")
        command_old = [
            'ffmpeg',
            '-y',
            '-f', 'alsa',
            '-i', 'default',
            '-f', 'rawvideo',
            '-acodec', 'aac',
            '-strict', '-2',
            '-vcodec', 'rawvideo',
            '-pix_fmt', 'bgr24',
            '-s', '1280x720',
            '-re',
            '-i', '-',
            '-f', 'flv',
            '-b:v', '1k',
            self.ru
        ]
        command = [
            'ffmpeg',
            '-y',
            '-f', 'rawvideo',
            '-vcodec', 'rawvideo',
            '-pix_fmt', 'bgr24',
            '-s', '720x480',
            '-re',
            '-i', '-',
            '-f', 'alsa',
            '-i', 'default',
            '-ar', '22050',
            '-map', '0:v:0',
            '-map', '1:a:0',
            '-f', 'flv',
            '-b:v', '1k',
            self.ru
        ]
        pipe = subprocess.Popen(command, stdin=subprocess.PIPE)
        while True:
            ct = Timer.timestamp()
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
                Control.force_exit()
        DanmuHandle.send("RESTART AT %s" % Timer.stamp2str(Timer.timestamp(), '%H:%M:%S'))
        print("PUSH THREAD EXIT")
        Control.force_exit()

    def _danmu_thread(self):
        """
        弹幕处理线程
        :return:
        """
        print("DANMU THREAD START")
        loop = asyncio.get_event_loop()
        loop.call_soon_threadsafe(DanmuHandle.run(loop))
        print("DANMU THREAD EXIT")

    def _clean_temp(self):
        """
        删除所有缓存
        :return:
        """
        for file in os.listdir(self.rp + 'temp'):
            os.remove(self.rp + 'temp/' + file)
            print("CLEAN IMAGE -> %s" % file.replace('.jpgx', ''))

    def _bgm_thread(self):
        """
        背景音乐线程
        :return:
        """
        print("MUSIC THREAD START")
        while not self.ef:
            music_list = AudioCtrl.audio_list().copy()
            for item in music_list:
                try:
                    self.bn = item['name']
                    command = [
                        'mpg123',
                        item['path']
                    ]
                    subprocess.Popen(command)
                    time.sleep(item['length'])
                except Exception as e:
                    print(e)
        print("MUSIC THREAD EXIT")

    def _timer_thread(self):
        """
        定时器线程
        :return:
        """
        print("TIMER THREAD START")
        Timer.timer()
        print("TIMER THREAD EXIT")

    def __del__(self):
        """
        退出时清理
        :return:
        """
        try:
            self._clean_temp()
        except Exception:
            pass

    def run(self):
        """
        运行
        :return:
        """
        self.config_init()
        Config.get('live') and threading.Thread(target=self._make_thread).start()
        Config.get('live') and threading.Thread(target=self._clean_thread).start()
        Config.get('bgm') and threading.Thread(target=self._bgm_thread).start()
        Config.get('live') and threading.Thread(target=self._push_thread).start()
        threading.Thread(target=self._timer_thread).start()
        Timer.timer_add(Extension.AutoReboot, 0)
        if Config.get('robot'):
            self._danmu_thread()
