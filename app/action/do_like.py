
# -*- coding: utf-8 -*-
'''
create by: 小宝
mail: 1435682155@qq.com
create date: 2019.8.18
Purpose: hah
'''
import sys
from common import config

config = config.open_accordant_config('doyin')
main_activity = "com.ss.android.ugc.aweme/com.ss.android.ugc.aweme.main.MainActivity"

actions = [
    {
        "step": 1,
        "desc": "打开app",
        "type": "open",
        "main_activity": main_activity,
    },
    {
        "step": 2,
        "desc": "截屏识图，判断符合后点赞",
        "type": "custom",
        "current": main_activity
    },
    {
        "step": 3,
        "desc": "翻页",
        "type": "swipe",
        "x1": config['center_point']['x'],
        "y1": config['center_point']['y'],
        "x2": config['center_point']['x'],
        "y2": config['center_point']['y'] - config['center_point']['ry'],
        "current": main_activity,
        "expect": ""
    }
]