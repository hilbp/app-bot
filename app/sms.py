# -*- coding: utf-8 -*-
'''
create by: 小宝
mail: 1435682155@qq.com
create date: 2019.8.11
Purpose: 短消息服务
Desc：将短消息(动态、心情、瞬间...)一键发布到多个平台
'''
import sys
import time

sys.path.append('./app')
from common.app import app
from common import config

# 导入支持平台的action
from action import sms_qq
from action import sms_soul

class sms(app):
    def __init__(self):
        self.config = config.open_accordant_config('sms')
        self.delay = float(self.config['delay']['value'])
        self.retry = int(self.config['retry']['value'])
        self.supported_app = ('qq', 'wechat', 'soul')
        
    def run(self):
        try:
            self.set_ime('ime_adb_keyboard')
            self.auto_send_sms()
            self.set_ime('ime_default_keyboard')
            exit('谢谢使用')
        except KeyboardInterrupt:
            self.set_ime('ime_default_keyboard')
            exit('谢谢使用')

    def auto_send_sms(self):
        app_list = self.config['app_send']['name']
        for app in app_list:
            if app not in self.supported_app: continue
            self.single_app_send(app)
            print('{}操作完成'.format(app))

    def single_app_send(self, app_name):
        file = 'sms_{}'.format(app_name)
        actions = eval(file).actions
        flg = False
        while True:
            for action in actions:
                if action['type'] ==  'open':
                    if not self._open_app(action['main_activity'], self.delay):
                        flg = True
                        break
                elif action['type'] == 'click':
                    if not self._click_operate(action['current'], action['x'], action['y'], self.delay, action['expect'], self.retry):
                        flg = True
                        break
                elif action['type'] == 'input':
                    # 唤起输入法
                    self._click_operate(action['current'], action['x'], action['y'], self.delay)
                    # 输入消息
                    cmd = 'shell am broadcast -a ADB_INPUT_TEXT --es msg {message}'.format(
                        message = self.config['send_content'][app_name] if self.config['send_content'][app_name] else self.config['send_content']['default']
                    )
                    self.adb.run(cmd)
                    flg = False
                    time.sleep(self.delay)
                else:
                    exit('未知异常')
            if not flg:
                break
    pass 
