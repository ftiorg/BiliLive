#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/8 下午 08:42
# @Author  : kamino

import cv2
import numpy
import os
from PIL import Image, ImageDraw, ImageFont


class ImageCtrl(object):

    @staticmethod
    def image_create(width=1270, height=720):
        image = numpy.zeros([height, width, 3], numpy.uint8)
        return image

    @staticmethod
    def image_read(path):
        return cv2.imread(path)

    @staticmethod
    def image_show(image, name='imshow', wait=0):
        cv2.imshow(name, image)
        cv2.waitKey(wait)

    @staticmethod
    def image_write(image, text, location=(0, 0), size=40, color=(255, 255, 255, 0), font=''):
        image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(image)
        if os.path.exists(font):
            font = ImageFont.truetype(font, size=size)
        else:
            font = None
        draw.text(location, str(text), font=font, fill=color)
        return cv2.cvtColor(numpy.asarray(image), cv2.COLOR_RGB2BGR)

    @staticmethod
    def image_resize(image, size=(1920, 1080)):
        return cv2.resize(image, size)

    @staticmethod
    def image_tostring(image):
        return image.tostring()

    @staticmethod
    def image_fromstring(string):
        return numpy.fromstring(string)

    @staticmethod
    def image_save(image, path):
        cv2.imwrite(path, image)

    @staticmethod
    def image_cover(image, cover, position=(0, 0)):
        image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        cover = Image.fromarray(cv2.cvtColor(cover, cv2.COLOR_BGR2RGB))
        image.paste(cover, position)
        return cv2.cvtColor(numpy.asarray(image), cv2.COLOR_RGB2BGR)
