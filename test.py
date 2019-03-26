#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/8 下午 07:07
# @Author  : kamino

import BiliLive

url = 'rtmp://127.0.0.1:1935/myapp/test'

if __name__ == '__main__':
    live = BiliLive.BiliLive()
    live.config('./config/config.json')
    live.make_image(show=True)
    # live.test()
