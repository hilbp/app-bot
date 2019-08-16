# -*- coding: utf-8 -*-
'''
create by: 小宝
mail: 1435682155@qq.com
create date: 2019.8.10
Purpose: 微信机器人
'''
import sys
import random
import time
import base64
from PIL import Image
import json

sys.path.append('./app')
from common import config
from common import comm
from common import screenshot
from common import debug
from common.app import app

class wechat(app):
    def __init__(self):
        self.config = config.open_accordant_config('wechat')
        self.delay = float(self.config['delay']['value'])
        self.retry = int(self.config['retry']['value'])
        screenshot.check_screenshot()
        # 朋友圈截图区域
        self.sns_region = self.get_sns_region()
        # 缓存好友信息
        self.temp = {}
        # 统计翻页
        self.page = 1
    pass

    # 应用运行入口
    def run(self):
        self.cmd_run()
        
    def cmd_run(self):  
        try:
            self.contacter_test()  
        except KeyboardInterrupt:
            self.set_ime('ime_default_keyboard')
            print('谢谢使用')
            exit(0)  

    # 好友检测
    def contacter_test(self):
        main_activity = self.config['main_activity']['name']
        while True:
            # 1.打开应用
            if not self._open_app(main_activity, self.delay):
                continue
            # 2.点击菜单【通讯录】
            if not self.clike_menu('menu_contact'):
                continue
            # 3.遍历好友列表
            self.loop_contacter_list()
            exit('over')
    pass
    
    # 循环通讯录列表
    def loop_contacter_list(self):
        # 【通讯录】列表初始化
        self.contact_list_init()
        while True:
            # 从配置获取列表中第一个好友的位置坐标
            x = self.config['first_contacter']['x']
            y = self.config['first_contacter']['y']
            row_margin = self.config['friend_list_row_margin']['value']
            # 点击列表中的4个人后向上滑动
            for i in range(4):
                print('对好友检测中...')
                # 对单个好友操作
                self.contacter_operate(x, y)
                print(self.temp)
                i += 1
                y += row_margin

            # 向上滑动好友列表
            self.swipe_contact_list()
    pass

    # 单个联系人的流水线操作
    def contacter_operate(self, x, y):
        # 点击坐标打开好友卡片
        self.open_friend_card(x, y)
        # 尝试打开朋友圈
        if not self.open_sns([x, y]):
            # 返回好友列表
            return
        # 打开朋友圈后的操作，拉取动态、截屏、提取文字、判断是否是好友
        self.handle_sns()
        # 返回好友列表
        self.back_friend_list()
    pass
    
    # 向上滑动好友列表
    def swipe_contact_list(self):
        x1 = self.config['list_init_swipe']['x']
        y1 = self.config['list_init_swipe']['y']
        x2 = self.config['list_init_swipe']['x']
        y2 = self.config['list_init_swipe']['y'] + self.config['list_init_swipe']['ry']
        delay = self.config['list_init_swipe']['delay']
        self.swipe_operate(x1, y1, x2, y2, self.delay, delay)
        self.page += 1
    pass

    # 【通讯录】列表初始化
    def contact_list_init(self):
        # 最先确认页面处于最顶叶
        self.sure_in_top()
        # 从文件恢复上一次中断的状态
        self.recovery_last_status()        
    pass
    
    # 从文件恢复上一次中断的状态
    def recovery_last_status(self):
        # 从文件读取前一次保存的状态
        content = self.get_line_from_file('wx_contacter.txt')
        if content:
            page = content['page'] -1
            for i in range(page):
                self.swipe_contact_list()
                i += 1
    pass

    # 最先确认页面处于最顶叶
    def sure_in_top(self):
        x1 = self.config['screen_center']['x']
        y1 = self.config['screen_center']['y']
        x2 = x1 + self.config['screen_center']['rx']
        y2 = y1 + self.config['screen_center']['ry']
        self.swipe_operate(x1, y1, x2, y2, self.delay)
    
    # 点击菜单
    def clike_menu(self, name):
        main_activity = self.config['main_activity']['name']
        x = self.config[name]['x']
        y = self.config[name]['y']
        if self._click_operate(main_activity, x, y, self.delay):
            return True
        return False
    pass

    # 打开好友卡片
    def open_friend_card(self, x, y):
        main_activity = self.config['main_activity']['name']
        friend_card = self.config['friend_card']['name']
        flg = self._click_operate(main_activity, x, y, self.delay, friend_card, self.retry)
        if not flg:
            # 可能原因：由于好友列表存在A、B、C这样的序号
            exit('未能打开好友卡片')
    pass

    # 打开朋友圈
    def open_sns(self, location):
        # 好友卡片截屏并文字提取
        image = self.screen_to_img()
        options = {}
        options["recognize_granularity"] = "big"
        res = comm.ocr_general(image, options)
        if res == False:
            exit(self.set_ime('ime_default_keyboard'))

        # 存储识别的好友昵称
        words_result = res['words_result']
        self.temp = {}
        self.temp['x'] = location[0]
        self.temp['y'] = location[1]
        self.temp['page'] = self.page
        self.temp['nickname'] = words_result[2]['words']
        self.temp['info'] = '{} | {}'.format(words_result[3]['words'], words_result[4]['words'])
        
        # 获取朋友圈按钮坐标
        more = words_result[-3]
        if more['words'] != '更多信息':
            print('可能是微信团队账号、文件传输账号、对方删除已经帐号、自己的账号，坑哦~')
            self.back_friend_list('friend_card')
            return False
        x = self.config['screen_center']['x']
        y = int(more['location']['top']) - self.config['button_more_to_sns_dist']['value']

        # 模拟点击朋友圈的按钮坐标
        friend_sns = self.config['friend_sns']['name']
        friend_card = self.config['friend_card']['name']
        flg = self._click_operate(friend_card, x, y, self.delay, friend_sns, self.retry)
        if not flg:
            print('可能朋友圈已关闭，好坑哦~')
            self.back_friend_list('friend_remark')
            return False
        return True
    pass

    # 返回好友列表
    def back_friend_list(self, current_activity = ''):
        main_activity = self.config['main_activity']['name']
        if current_activity == '':
            current = self.config['friend_sns']['name']
        else:
            current = self.config[current_activity]['name']
        self.back_expect_page(current, main_activity, self.delay, self.retry)
    
    # 朋友圈处理
    def handle_sns(self):
        # 滑动朋友圈拉取动态
        x1 = self.config['screen_center']['x']
        y1 = self.config['screen_center']['y'] + self.config['screen_center']['ry']
        x2 = self.config['screen_center']['x']
        y2 = self.config['screen_center']['y']
        sns_swipe_num = int(self.config['sns_swipe_num']['value'])
        for i in range(sns_swipe_num):
            self.swipe_operate(x1, y1, x2, y2, self.delay)
            i += 1

        # 朋友圈截屏并调用接口文字识别
        image = self.screen_to_img('', self.sns_region)
        res = comm.occ_basic_general(image)
        if res == False:
            exit(self.set_ime('ime_default_keyboard'))

        # 判断是否是好友
        flg = self.test_is_friend(res)
        self.info_save_file('wx_contacter.txt', self.temp)
        if not flg:
            self.info_save_file('wx_notfriend.txt', self.temp)
    pass
    
    # 判断是否是好友
    def test_is_friend(self, res):
        if res['words_result_num'] == 0:
            self.temp['status'] = '该好友屏蔽了你'
            return False
        last_word = res['words_result'][-1]['words']
        self.temp['status'] = last_word
        index = last_word.find('朋友仅展示')
        if index >= 0:
            return True
        index = last_word.find('非对方的朋友')
        if index >= 0:
            return False
        if res['words_result_num'] < 3:
            self.temp['status'] = '该好友屏蔽了你'
            return False

        return True
    pass

    # 朋友圈截图区域设置，初始化只调用一次
    def get_sns_region(self):
        locaton = self.config['friend_sns_img_region']
        del locaton['desc']
        region  = tuple([var for var in locaton.values()])
        return region
    pass

    # 把非好友信息保存到txt
    def info_save_file(self, name, item):
        name = './tmp/{}'.format(name)
        temp = json.dumps(item, ensure_ascii = False)
        with open(name, 'a') as f:  
            # f.seek(0, 0)  
            # content = f.read()            
            # f.write(temp + '\n' + content)
            f.write(temp + '\n')
    pass

    # 从文件读取保存的状态数据
    def get_line_from_file(self, name):
        name = './tmp/{}'.format(name)
        with open(name, 'a+') as f:
            f.seek(0,0)
            content =  f.readlines()
        if not content:
            return False    
        return json.loads(content[-1])
    pass 