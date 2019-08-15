# -*- coding: utf-8 -*-
'''
create by: 小宝
mail: 1435682155@qq.com
create date: 2019.8.11
Purpose: QQ机器人
'''
import sys
import time
import random

sys.path.append('./app')
from common.auto_adb import auto_adb
from common import config
from common import debug
from common import function
from common.app import app

class qq(app):
    def __init__(self):
        super().__init__()
        self.config = config.open_accordant_config('qq')
        self.delay = int(self.config['delay']['value'])
        self.retry_count = int(self.config['retry_count']['value'])
        # app运行前设置adb keyboard输入法
        self.set_ime('ime_adb_keyboard')
    
    # 入口
    def run(self):
        self.reply_message()

    # 一直给指定的人发送消息
    def reply_message(self):
        # 打开qq
        self.open_qq()
        # 点击【消息】
        self.tap_menu('menu_message')
        # 点击特定联系人坐标
        self.tap_operate('one_chat')
        # 发送消息
        while True:
            message = random.choice(self.config['default_word']['value'])
            self.send_message(message)

    # 打开qq
    def open_qq(self):
        print("正在打开qq主页")
        main_activity = self.config['main_activity']['name']
        if self._open_app(main_activity, self.delay):
            return True
        return False

    # 模拟点击菜单
    def tap_menu(self, name):
        print('正在点击菜单%s' % name)
        current = self.is_focused_activity('main_activity')
        if not current:
            return False
        else:
            self.tap_operate(name)
            return True 
    
    # 点击操作
    def tap_operate(self, name):
        x = self.config[name]['x']
        y = self.config[name]['y']
        self.click(x, y)
        time.sleep(self.delay)


    # 模拟点击菜单后判断是否打开了目标activity
    def is_focused_activity(self, name):
        activity = self.config[name]['name']
        if self._is_focused_activity_super(activity):
            return True
        return False

    # 发消息，支持主动打招呼和被动回复
    def send_message(self, message):
        # 唤起输入法
        self.tap_operate('chat_input')
        # 输入消息
        cmd = 'shell am broadcast -a ADB_INPUT_TEXT --es msg {message}'.format(
            message = message
        )
        self.adb.run(cmd)
        time.sleep(self.delay)
        # 发送消息
        self.tap_operate('send_button')
        print("消息发送完成：%s" % message)
