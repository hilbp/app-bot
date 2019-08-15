
# -*- coding: utf-8 -*-
'''
create by: 小宝
mail: 1435682155@qq.com
create date: 2019.8.17
Purpose: qq动作编排
'''
import sys
from common import config

config = config.open_accordant_config('sms')
main_activity = "cn.soulapp.android/cn.soulapp.android.ui.main.MainActivity"
input_activity = "cn.soulapp.android/cn.soulapp.android.ui.publish.NewPublishActivity"

actions = [
    {
        "step": 1,
        "desc": "打开soul",
        "type": "open",
        "main_activity": main_activity
    },
    {
        "step": 2,
        "desc": "点击【发布瞬间】",
        "type": "click",
        "x": config['soul_send_moment']['x'],
        "y": config['soul_send_moment']['y'],
        "current": main_activity,
        "expect": input_activity
    },
    {
        "step": 3,
        "desc": "输入内容",
        "type": "input",
        "x": config['soul_text_input']['x'],
        "y": config['soul_text_input']['y'],
        "current": input_activity,
        "expect": ""
    },
    {
        "step": 4,
        "desc": "点击右上角【发布】",
        "type": "click",
        "x": config['soul_send_button']['x'],
        "y": config['soul_send_button']['y'],
        "current": input_activity,
        "expect": main_activity
    }
]