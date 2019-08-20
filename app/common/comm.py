# -*- coding: utf-8 -*-
'''
通用函数
'''
import requests
from common import config
from common import ai
from PIL import Image
import math
import os

# 通用orc
def occ_basic_general(image):
    return ai.bae_ocr_basic_general(image)

# 通用orc(含位置信息)
def ocr_general(image, options):
    return ai.bae_ocr_general(image, options)

# 调用机器人接口获取回复内容，这个机器人很黄很污啊
def get_reply_content(message):
    return ai.qingyun_bot_reply(message)

# 人脸检测与分析
def face_detectface():
    return ai.qq_face_detectface()

# 优化图片
def resize_image(origin_img, optimize_img, threshold):
    file_size = os.path.getsize(origin_img)
    with Image.open(origin_img) as im:
        if file_size > threshold:
            width, height = im.size

            if width >= height:
                new_width = int(math.sqrt(threshold / 2))
                new_height = int(new_width * height * 1.0 / width)
            else:
                new_height = int(math.sqrt(threshold / 2))
                new_width = int(new_height * width * 1.0 / height)

            resized_im = im.resize((new_width, new_height))
            resized_im.save(optimize_img)
        else:
            im.save(optimize_img)
