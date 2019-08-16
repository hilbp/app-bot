# -*- coding: utf-8 -*-
'''
各种AI接口调用
'''
import requests
from requests import RequestException
from aip import AipOcr
from common import config
from common import TencentAPI
from common.TencentAPIMsg import TencentAPIMsg

config = config.open_accordant_config('common')

# 腾讯AI配置，尽量自己去申请APPID、APPKEY
def qq_ai_set():
    APPID = config['qq_ai']['APP_ID']
    APPKEY = config['qq_ai']['API_KEY']
    return (APPID, APPKEY)

# 腾讯通用ocr
def qq_orc_general(image):
    (APPID,APPKEY) = qq_ai_set()
    tx= TencentAPIMsg(APPID,APPKEY)
    Req_Dict={}
    Req_Dict['image'] = tx.get_img_base64str('./tmp/screen.png')
    url = TencentAPI.TencentAPI['ocr_generalocr']['APIURL']
    tx.init_req_dict(req_dict=Req_Dict)
    resp = requests.post(url, data=Req_Dict)
    # TODO:
    print(resp.json())

#创建bae对象，尽量自己去申请APPID、APPKEY
def create_bae():
    # 百度AI配置
    APP_ID = config['bae_ai']['APP_ID']
    API_KEY = config['bae_ai']['API_KEY']
    SECRET_KEY = config['bae_ai']['SECRET_KEY']
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    return client

# 百度通用orc
def bae_ocr_basic_general(image):
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

# 调用机器人接口获取回复内容，这个机器人很黄很污啊
def qingyun_bot_reply(message):
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

# 腾讯机器人接口
def qq_bot_reply(message):
    # TODO:
    pass
