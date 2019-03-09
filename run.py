#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/8 下午 07:07
# @Author  : kamino

import BiliLive

if __name__ == '__main__':
    live = BiliLive.BiliLive('2019-12-21 00:00:00', 'rtmp://xxx')
    live.run()
