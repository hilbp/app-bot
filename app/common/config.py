# -*- coding: utf-8 -*-
"""
调取配置文件和屏幕分辨率的代码
"""
import os
import sys
import json
import re

from common.auto_adb import auto_adb

adb = auto_adb()


def open_accordant_config(config_name = ''):
    """
    调用配置文件
    """
    if config_name == '':
        config_name = 'config'
        
    screen_size = _get_screen_size()
    config_file = "{path}/conf/{screen_size}/{config_name}.json".format(
        path = sys.path[0],
        screen_size = screen_size,
        config_name = config_name
    )

    # 根据分辨率查找配置文件
    if os.path.exists(config_file):
        with open(config_file, 'rb') as f:
            # print("正在从 {} 加载配置文件".format(config_file))
            return json.load(f)
    else:
        with open('{}/conf/default/{}.json'.format(sys.path[0], config_name), 'rb') as f:
            # print("Load default config")
            return json.load(f)


def _get_screen_size():
    """
    获取手机屏幕大小
    """
    size_str = adb.get_screen()
    m = re.search(r'(\d+)x(\d+)', size_str)
    if m:
        return "{height}x{width}".format(height=m.group(2), width=m.group(1))
    return "1920x1080"
