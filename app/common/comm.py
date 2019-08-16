# -*- coding: utf-8 -*-
'''
通用函数
'''
import requests
from common import config
from common import ai

# 通用orc
def occ_basic_general(image):
    return ai.bae_ocr_basic_general(image)

# 通用orc(含位置信息)
def ocr_general(image, options):
    return ai.bae_ocr_general(image, options)

# 调用机器人接口获取回复内容，这个机器人很黄很污啊
def get_reply_content(message):
    return ai.qingyun_bot_reply(message)
