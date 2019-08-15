
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
main_activity = "com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity"
zone_activity = "com.tencent.mobileqq/cooperation.qzone.QzoneFeedsPluginProxyActivity"
input_activity = "com.tencent.mobileqq/cooperation.qzone.QzonePublishMoodProxyActivity"

actions = [
    {
        "step": 1,
        "desc": "打开qq",
        "type": "open",
        "main_activity": main_activity,
    },
    {
        "step": 2,
        "desc": "点击菜单中的【动态】",
        "type": "click",
        "x": config['qq_menu_news']['x'],
        "y": config['qq_menu_news']['y'],
        "current": main_activity,
        "expect": ""
    },
    {
        "step": 3,
        "desc": "点击左上空间图标",
        "type": "click",
        "x": config['qq_zone_icon']['x'],
        "y": config['qq_zone_icon']['y'],
        "current": main_activity,
        "expect": ""
    },
    {
        "step": 4,
        "desc": "点击右上角的【+】号",
        "type": "click",
        "x": config['qq_add_icon']['x'],
        "y": config['qq_add_icon']['y'],
        "current": zone_activity,
        "expect": ""
    },
    {
        "step": 5,
        "desc": "点击【说说】",
        "type": "click",
        "x": config['qq_say_link']['x'],
        "y": config['qq_say_link']['y'],
        "current": zone_activity,
        "expect": ""    
    },
    {
        "step": 6,
        "desc": "输入内容",
        "type": "input",
        "x": config['qq_text_input']['x'],
        "y": config['qq_text_input']['y'],
        "current": input_activity,
        "expect": "" 
    },
    {
        "step": 7,
        "desc": "点击右上角【发表】",
        "type": "click",
        "x": config['qq_send_button']['x'],
        "y": config['qq_send_button']['y'],
        "current": input_activity,
        "expect": ""
    }
]