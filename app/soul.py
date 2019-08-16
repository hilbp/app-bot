# -*- coding: utf-8 -*-
'''
create by: 小宝
mail: 1435682155@qq.com
create date: 2019.8.3
Purpose: soul机器人
'''

import sys
import random
import time
import base64
from PIL import Image
import signal

sys.path.append('./app')
from common import config
from common import comm
from common import screenshot
from common.app import app

class soul(app):
    def __init__(self):
        super().__init__()
        screenshot.check_screenshot()
        self.config = config.open_accordant_config('soul')
        self.delay = float(self.config['delay']['value'])
        self.retry = int(self.config['retry']['value'])
    
    # soul入口
    def run(self):
        self.cmd_run()
        
    def cmd_run(self):
        # app运行前设置adb keyboard输入法
        self.set_ime('ime_adb_keyboard')
        while True:
            try:
                key = input(
                    "\n=========***欢迎使用soul-bot***=========\n"+
                    "请输入序号选择功能：\n"+
                    "> 1：灵魂匹配并主动打招呼\n"+
                    "> 2：来消息时自动回复\n"+
                    "> 3：来消息时手动回复\n"+
                    "> 4：与特定对象聊天\n"+
                    "> 0：退出程序\n"+
                    "=======================================\n"
                    "请输入[1/2/3/4/0]："
                )
                key = int(key)
                if key == 1: return self.loop_match(10) # 灵魂匹配
                elif key == 2: return self.loop_replay_bot() # 调用机器人接口回复
                elif key == 3: return self.loop_replay_manual() # 手动回复
                elif key == 4: return self.loop_chat_one() # 与特定的个人聊天
                elif key == 0: 
                    self.set_ime('ime_default_keyboard') # app运行完恢复默认输入法
                    exit('谢谢使用')
            except ValueError:
                # print('按提示输入呀~老铁')
                continue
            except KeyboardInterrupt:
                # print('>>>已屏蔽Ctrl+C，输入0退出程序')
                continue
            
    # 循环进行灵魂匹配
    def loop_match(self, num):
        while True:
            # 1.打开soul主页
            if not self.open_soul():
                continue
            # 2.点击底部菜单中的【星球】
            if not self.tap_menu('menu_star'):
                continue
            # 3.点击灵魂匹配
            if not self.tap_soul_match():
                continue
            # 4.打招呼
            if not self.say_hello():
                continue
            # 5.退出聊天窗口
            self.back_main_page()
    
    # 监听消息列表，有消息提示时通过机器人被动回复
    def loop_replay_bot(self):
        while True:
            # 0.打开soul
            if not self.open_soul():
                continue
            # 1.打开底部【聊天】菜单
            if not self.tap_menu('menu_chat'):
                continue
            # 2.截屏并获取坐标
            location = self.get_location()
            if not location:
                print('没有未读消息，程序继续监听，按ctrl+c终止')
                continue
            # 3.打开会话窗口
            x, y = location[0]
            if not self.open_chat_window(x, y):
                continue
            # 4.截屏、提取文字并识别
            word = self.handle_img_ocr()
            # 5.调用机器人接口
            content = comm.get_reply_content(word)
            # 6.回复消息
            if not self.send_message(content):
                continue
            print('收到的消息：{word}\n回复的消息：{content}'.format(
                word = word,
                content = content
            ))
            # 6. 返回消息列表
            self.back_main_page()
    
    # 监听消息列表，有消息提示时提醒手动回复
    def loop_replay_manual(self):
        while True:
            # 0.打开soul
            if not self.open_soul():
                continue
            # 1.打开底部【聊天】菜单
            if not self.tap_menu('menu_chat'):
                continue
            # 2.截屏并获取坐标
            location = self.get_location()
            if not location:
                print('没有未读消息，程序继续监听，按ctrl+c终止')
                continue
            # 3.打开会话窗口
            x, y = location[0]
            if not self.open_chat_window(x, y):
                continue
            # 4.截屏、提取文字并识别
            word = self.handle_img_ocr()
            # 5.将消息显示在屏幕上并提醒
            content = self.reply_manual(word)
            if not content:
                continue
            # 6.回复消息
            if not self.send_message(content):
                continue
            print('收到的消息：{word}\n回复的消息：{content}'.format(
                word = word,
                content = content
            ))
            # 6. 返回消息列表
            self.back_main_page()
    
    # 与特定对象手动聊天
    def loop_chat_one(self):
        
        while True:
            # 1.确保用户已打开会话窗口
            current = self.is_focused_activity('chat_window_activity')
            if not current:
                print('需手动打开你想要聊天的人的对话窗口！')
                continue
            # 2.0 需创建一个线程异步保持屏幕常亮
            # threading.Thread(target = self.keep_screen_light).run()
            # 2.1 回复消息
            while True:
                content = input("请输入回复内容：")
                if content: break
            
            self.send_message(content)

    # 打开soul
    def open_soul(self):
        print("正在打开soul主页")
        main_activity = self.config['main_activity']['name']
        if self._open_app(main_activity, self.delay):
            return True
        return False

    # 模拟点击菜单
    def tap_menu(self, name):
        print('正在点击菜单%s' % name)
        return self.tap_operate('main_activity', name)
    
    # 模拟点击灵魂匹配的按钮
    def tap_soul_match(self):
        print('正在点击灵魂匹配的按钮')
        return self.tap_operate('main_activity', 'soul_match')
        

    # 主动打招呼
    def say_hello(self):
        # 由于灵魂匹配需要等待几秒钟 当程序执行到这里时有可能还未能匹配成功 所以需要加以判断
        for i in range(self.retry):
            current = self.is_focused_activity('chat_window_activity')
            i += 1
            if current == True:
                print('正在打招呼')
                message = random.choice(self.config['default_word']['value'])
                self.send_message(message)
                return True
            else:
                is_soul_match_activity = self.is_focused_activity('soul_match_activity')
                if is_soul_match_activity:
                    time.sleep(self.delay * 2)
                    print('貌似还未匹配成功，再等等哦... %d' % i)
                    continue
        return False

    # 发消息，支持主动打招呼和被动回复
    def send_message(self, message):
        activity = 'chat_window_activity'
        current = self.is_focused_activity(activity)
        if current:
            # 唤起输入法
            self.tap_operate(activity, 'chat_input')
            # 输入消息
            cmd = 'shell am broadcast -a ADB_INPUT_TEXT --es msg {message}'.format(
                message = message
            )
            self.adb.run(cmd)
            time.sleep(self.delay)
            # 发送消息
            self.tap_operate(activity, 'send_button')
            print("消息发送完成")
            return True
        else:
           return False

    # 模拟点击菜单后判断是否打开了目标activity
    def is_focused_activity(self, name):
        activity = self.config[name]['name']
        if self._is_focused_activity_super(activity):
            return True
        return False
        
    # 模拟返回按键
    def back_main_page(self):
        current = self.config['chat_window_activity']['name']
        expect = self.config['main_activity']['name']
        self.back_expect_page(current, expect, self.delay, self.retry)
    
    # 点击操作
    def tap_operate(self, current, name):
        x = self.config[name]['x']
        y = self.config[name]['y']
        current = self.config[current]['name']
        return self._click_operate(current, x, y, self.delay)
    
    # 获取消息点坐标
    def get_location(self):
        im = screenshot.pull_screenshot().convert('L')
        height = im.size[1]
        i, j = (1025, 0)
        location = []
        while j < height:
            pixel = im.getpixel((i, j))
            if pixel == 128:
                location.append((i, j))
                j += 41
                break
            j += 1
        if not location:
            return False

        return location

    # 打开聊天的对话框
    def open_chat_window(self, x, y):
        current = self.config['main_activity']['name']
        return self._click_operate(current, x, y, self.delay)
    
    # 截屏并文字提取、识别，返回一条需要回复的内容
    def handle_img_ocr(self):
        current = self.is_focused_activity('chat_window_activity')
        if current == False:
            return self.tap_menu('menu_chat')
        image = self.screen_to_img()
        # 文字识别
        res = comm.occ_basic_general(image)
        if res == False:
            exit(self.set_ime('ime_default_keyboard'))
        return res['words_result'][-2]['words']

    def reply_manual(self, word):
        if not word:
            return False
        # is_reply = tkinter.messagebox.askokcancel('收到消息', '“%s”\n是否回复？' % word)
        # 注意：在输入消息时有可能会息屏，所以应该发送亮屏信息
        cmd = 'shell input keyevent 224'
        self.adb.run(cmd)
        print("收到消息：%s" % word)
        while True:
            content = input("输入回复内容:")
            if content: break
        return content
    
    async def keep_screen_light(self):
        while True:
            print('发送了点亮屏幕的命令')
            cmd = 'shell input keyevent 224'
            self.adb.run(cmd)
        pass
    
        
        



