# -*- coding: utf-8 -*-
'''
通用函数
'''
import random
import requests
import urllib
from urllib import parse
from aip import AipOcr
from requests import RequestException
from common import config


# 百度AI相关配置
APP_ID = '16953366'
API_KEY = 'tv8BpgDWqX6PmRxtkqrxo5Fj'
SECRET_KEY = 'aKWFhIRmKMP4S9FGzERAdhED5wg2eEHV'

# 通用orc
def occ_basic_general(image):
    return bae_occ_basic_general(image)

# 通用orc(含位置信息)
def ocr_general(image, options):
    return bae_ocr_general(image, options)

#创建bae对象
def create_bae():
    # config_data = config.open_accordant_config('common')
    # APP_ID = config_data['bae_config']['APP_ID']
    # API_KEY = config_data['bae_config']['API_KEY']
    # SECRET_KEY = config_data['bae_config']['SECRET_KEY']
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    return client

# 百度通用orc
def bae_occ_basic_general(image):
    for i in range(10):
        try:
            bae_client = create_bae()
            res = bae_client.basicGeneral(image)
            if 'error_code' in res.keys():
                print(res['error_msg'])
                return False
        except ConnectionError:
            i += 1
            print('调用百度通用ocr接口出现异常，正在第{}次重试...'.format(i))
            continue
        else:
            return res
    
    print('调用百度通用ocr接口失败，程序退出')
    return False
pass

# 百度通用orc(含位置信息)
def bae_ocr_general(image, options):
    for i in range(10):
        try:
            bae_client = create_bae()
            res = bae_client.general(image, options)
            if 'error_code' in res.keys():
                print(res['error_msg'])
                return False
        except ConnectionError:
            i += 1
            print('调用百度通用ocr接口出现异常，正在第{}次重试...'.format(i))
            continue
        else:
            return res

    print('调用百度通用ocr(含位置信息)接口失败，程序退出')
    return False
pass

# 调用机器人接口获取回复内容，这个机器人很黄很污啊
def get_reply_content(message):
    default = '我还是个孩子啊，你说啥~'
    host = 'http://api.qingyunke.com/api.php?key=free&appid=0&msg={message}'.format(
        message = message
    )
    s = requests.session()
    s.keep_alive = False
    res = requests.get(host).json()
    if res['result'] == 0:
        return res['content']  
    return default
pass
