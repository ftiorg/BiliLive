#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/8 下午 07:07
# @Author  : kamino

import BiliLive
import threading
import time


def work(i=123):
    print(i)
    time.sleep(5)
    print(i + 1)


if __name__ == '__main__':
    # live = BiliLive.BiliLive()
    # live.make_image(show=True)

    # BiliLive.DanmuHandle.send('你好啊')
    # print(BiliLive.StudyExt.SignedList())
    # print(BiliLive.StudyExt.SignRank())
    # print(BiliLive.Auth.get_uname('16011372'))                                                                                      time=time))
    # print(BiliLive.RobotReply.reply(1, 1, 'hello'))
    # print(BiliLive.StudyExt.ChgColor('color red'))

    threading.Thread(target=BiliLive.Timer.timer).start()
    BiliLive.Timer.timer_add(work(), BiliLive.Timer.timestamp() + 5)
    BiliLive.Timer.timer_add(work(), BiliLive.Timer.timestamp() + 10)
