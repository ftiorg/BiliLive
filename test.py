#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/8 下午 07:07
# @Author  : kamino

import BiliLive
import threading
import time


def work(i):
    t = i[0]
    for i in range(10):
        print(t)
        t += 1
        time.sleep(1)


if __name__ == '__main__':
    # live = BiliLive.BiliLive()
    # live.make_image(show=True)

    # BiliLive.DanmuHandle.send('你好啊')
    # print(BiliLive.Extension.SignedList())
    # print(BiliLive.Extension.SignRank())
    # print(BiliLive.Auth.get_uname('16011372'))                                                                                      time=time))
    # print(BiliLive.RobotReply.reply(1, 1, 'hello'))
    # print(BiliLive.Extension.ChgColor('color red'))

    threading.Thread(target=BiliLive.Timer.timer).start()
    BiliLive.Timer.timer_add(action=work, arg=(1,), runat=BiliLive.Timer.timestamp() + 5)
    BiliLive.Timer.timer_add(action=work, arg=(100,), runat=BiliLive.Timer.timestamp() + 10)
