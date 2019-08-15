# -*- coding: utf-8 -*-
'''
create by: 小宝
mail: 1435682155@qq.com
create date: 2019.8.3
Purpose: base class be used to app extends
'''
import sys
import re
import random
import time
import base64
from PIL import Image

sys.path.append('../')
from common.auto_adb import auto_adb
from common import config
from common import function
from common import screenshot
from common import debug

class app():
    adb = auto_adb()

    def __init__(self):
        # 检查设备是否连接
        self.adb.test_device()
        # 打印设备信息
        # debug.dump_device_info()
        pass

    # 打开应用
    def _open_app(self, main_activity, delay):
        current = self._is_focused_activity_super(main_activity)
        if current:
            return True
        else:
            cmd = 'shell am start -n {activity}'.format(
                activity = main_activity
            )
            self.adb.run(cmd)
            time.sleep(delay)
            current = self._is_focused_activity_super(main_activity)
            if current:
                return True
            else:
                print('目前未能显示主页窗口可能原因：息屏状态、被弹窗覆盖等，重试中...')
                return False
    pass

    # 模拟点击菜单后判断是否打开了目标activity
    def _is_focused_activity_super(self, activity):
        # 获取当前的activity
        cmd = 'shell dumpsys window | findstr mFocusedWindow'
        output = self.adb.run(cmd)
        # print(output)
        index = output.find(activity, 0, len(output))
        if index < 0 :
            return False
        else:
            return True
    pass

        
    # 设置输入法
    def set_ime(self, ime):
        config_data = config.open_accordant_config('common')
        name = config_data[ime]['name']

        # 1.检测输入法是否安装
        cmd = 'shell ime list -a'
        output = self.adb.run(cmd)
        index = output.find(name, 0, len(output))
        if index < 0 :
            print('未安装{}输入法，安装后使用！'.format(name))
            exit(0)

        # 2.输入法设置
        cmd = 'shell ime set {}'.format(name)
        output = self.adb.run(cmd)
        index = output.find('selected', 0, len(output))
        if index < 0 :
            print('设置{}输入法失败，手动设置后使用'.format(name))
            exit(0)
    pass
    
    # 新定义的点击操作
    def _click_operate(self, current, x, y, delay, expect = '', retry = 0):
        if not self._is_focused_activity_super(current):
            return False
        cmd = 'shell input tap {x} {y}'.format(
            x=x + self._random_bias(10),
            y=y + self._random_bias(10)
        )
        self.adb.run(cmd)
        time.sleep(delay)
        if expect == '':
            return True

        for i in range(retry):
            i += 1
            if self._is_focused_activity_super(expect):
                return True
        return False
    pass

    # 点击操作
    def click(self, x, y):
        cmd = 'shell input tap {x} {y}'.format(
            x=x + self._random_bias(10),
            y=y + self._random_bias(10)
        )
        self.adb.run(cmd)
    pass
    
    # 点击区域随机偏置
    def _random_bias(self, num):
        return random.randint(-num, num)
    pass
    
    # 滑动屏幕
    def swipe_operate(self, x1, y1, x2, y2, delay, duration = 200):
        cmd = 'shell input swipe {x1} {y1} {x2} {y2} {duration}'.format(
            x1 = x1,
            y1 = y1,
            x2 = x2,
            y2 = y2,
            duration = duration
        )
        self.adb.run(cmd)
        time.sleep(delay)
    pass

    # 模拟返回按键
    def back_expect_page(self, current_activity, expect_activity, delay, retry):
        cmd = 'shell input keyevent 4'
        is_current_activity = self._is_focused_activity_super(current_activity)
        if is_current_activity:
            for i in range(retry):
                self.adb.run(cmd)
                i += 1
                time.sleep(delay)
                is_expect_activity = self._is_focused_activity_super(expect_activity)
                if is_expect_activity:
                    return True
                print('已完成操作，尝试返回{}'.format(i))
        return False
    pass

    # 截屏返回图像数据
    def screen_to_img(self, name = '', region = ()):
        im = screenshot.pull_screenshot()
        if not name:
            name = './tmp/screen.png'
        if region:
            crop_img = im.crop(region)
            crop_img.save(name)
        with open(name, 'rb') as bin_data:
            image = bin_data.read()
        return image
    pass

    

    
    

        
        

    
        
        



