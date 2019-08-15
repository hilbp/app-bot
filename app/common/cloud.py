# -*- coding: utf-8 -*-
'''
create by : 小宝
create date : 2019.8.10
Purpose:  调用各种云接口
'''

from aip import AipOcr

# 创建bae ai接口调用
def bae_ai():
    APP_ID = '16953366'
    API_KEY = 'tv8BpgDWqX6PmRxtkqrxo5Fj'
    SECRET_KEY = 'aKWFhIRmKMP4S9FGzERAdhED5wg2eEHV'
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    return client