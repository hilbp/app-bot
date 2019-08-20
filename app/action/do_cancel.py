
# -*- coding: utf-8 -*-
'''
create by: 小宝
mail: 1435682155@qq.com
create date: 2019.8.18
Purpose: cancel like star
'''
import sys
from common import config

config = config.open_accordant_config('doyin')
main_activity = "com.ss.android.ugc.aweme/com.ss.android.ugc.aweme.main.MainActivity"
video_activity = "com.ss.android.ugc.aweme/com.ss.android.ugc.aweme.detail.ui.DetailActivity"

actions = [
    {
        "step": 1,
        "desc": "打开app",
        "type": "open",
        "main_activity": main_activity,
    },
    {
        "step": 2,
        "desc": "底部菜单【我】",
        "type": "click",
        "x": config['menu_mine']['x'],
        "y": config['menu_mine']['y'],
        "current": main_activity,
        "expect": ""
    },
    {
        "step": 3,
        "desc": "选项卡【喜欢】",
        "type": "click",
        "x": config['like_count']['x'],
        "y": config['like_count']['y'],
        "current": main_activity,
        "expect": ""
    },
    {
        "step": 4,
        "desc": "第一个视频",
        "type": "click",
        "x": config['first_video']['x'],
        "y": config['first_video']['y'],
        "current": main_activity,
        "expect": ""
    },
    {
        "step": 5,
        "desc": "取消点赞",
        "type": "click",
        "x": config['like_star']['x'],
        "y": config['like_star']['y'],
        "current": video_activity,
        "expect": ""
    },
    {
        "step": 6,
        "desc": "返回",
        "type": "back",
        "current": video_activity,
        "expect": main_activity
    },
]