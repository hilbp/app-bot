# -*- coding: utf-8 -*-
"""
这是debug的代码，当DEBUG_SWITCH开关开启的时候，会将各种信息存在本地，方便检查故障
"""
import os
import sys
import shutil
import math
from PIL import ImageDraw
import platform
from common.auto_adb import auto_adb

if platform.system() == 'Windows':
    os.chdir(os.getcwd().replace('\\common', ''))
    path_split = "\\"
else:
    os.chdir(os.getcwd().replace('/common', ''))
    path_split = '/'
 
adb = auto_adb()
def dump_device_info():
    """
    显示设备信息
    """
    size_str = adb.get_screen()
    device_str = adb.test_device_detail()
    phone_os_str = adb.test_device_os()
    density_str = adb.test_density()
    print("""**********
Screen: {size}
Density: {dpi}
Device: {device}
Phone OS: {phone_os}
Host OS: {host_os}
Python: {python}
**********""".format(
        size=size_str.replace('\n', ''),
        dpi=density_str.replace('\n', ''),
        device=device_str.replace('\n', ''),
        phone_os=phone_os_str.replace('\n', ''),
        host_os=sys.platform,
        python=sys.version
    ))
