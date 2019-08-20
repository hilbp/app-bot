# -*- coding: utf-8 -*-
'''
create by: 小宝
mail: 1435682155@qq.com
create date: 2019.8.11
Purpose: hehe
Desc：just do it~
'''
import sys
import time
import os
import shutil

sys.path.append('./app')
from common.app import app
from common import config
from common import screenshot
from common import comm

# 导入支持平台的action
# from action import dy_like

class doyin(app):
    def __init__(self):
        super().__init__()
        screenshot.check_screenshot()
        self.config = config.open_accordant_config('doyin')
        self.delay = float(self.config['delay']['value'])
        self.retry = int(self.config['retry']['value'])
        pass
        
    def run(self):
        self.run_cmd()

    def run_cmd(self):
        try:
            key = input(
                "\n=========***欢迎使用doyin-bot***=========\n"+
                "请输入序号选择要操作的功能：\n"+
                "> 1：寻找美女并点赞\n"+
                "> 2：取消点赞\n"+
                "> 0: 退出程序\n"+
                "=======================================\n"
                "请输入[1/2/0]："
            )
            key = int(key)
            if key == 1:
                self.search_dest()
            elif key == 2:
                self.cancel_like()
            elif key == 0:
                exit('谢谢使用')
        except KeyboardInterrupt:
            exit('谢谢使用')

    def search_dest(self):
        from action import do_like
        while True:
            self.action_schedule('do_like', do_like)

    def cancel_like(self):
        from action import do_cancel
        while True:
            self.action_schedule('do_cancel', do_cancel)

    def action_schedule(self, action_name, action_file):
        actions = action_file.actions
        flg = True
        while True:
            for action in actions:
                if action['type'] ==  'open':
                    if not self._open_app(action['main_activity'], self.delay):
                        flg = False
                        break
                elif action['type'] == 'click':
                    if not self._click_operate(action['current'], action['x'], action['y'], self.delay, action['expect'], self.retry):
                        flg = False
                        break
                elif action['type'] == 'custom':
                    self.handle_custom_operate(action_name, action)
                elif action['type'] == 'swipe':
                    self._swipe_page(action['x1'], action['y1'], action['x2'], action['y2'])
                elif action['type'] == 'back':
                    self.back_expect_page(action['current'], action['expect'], self.delay, self.retry)
                else:
                    exit('未知异常') 
            if flg:
                break

    def handle_custom_operate(self, action_name, action):
        if action_name == 'do_like':
            return self._handle_screenshot(action)
            

    # 滑屏翻页
    def _swipe_page(self, x1, y1, x2, y2):
        self.swipe_operate(x1, y1, x2, y2, self.delay)

    # 截屏及相关操作
    def _handle_screenshot(self, action):
        # 1.截屏优化图片
        time.sleep(1)
        self.screen_to_img()
        comm.resize_image('./tmp/screen.png', './tmp/optimized.png', 1024*1024)
        # 2.调用接口
        res = comm.face_detectface()
        if res == False:
            return False
        # 3.判断处理
        is_dest = self._is_dest(res['face_list'], (0, 10), (80, 100), (0, 100))
        # 4.保存图片
        if is_dest != False:
            print('是个美人儿~点赞走一波')
            # 点赞
            x = self.config['like_star']['x']
            y = self.config['like_star']['y']
            self._click_operate(action['current'], x, y, self.delay, '', self.retry)
            self._img_save(is_dest['beauty'])
            return True
        return False

    # 满足条件的图片保存
    def _img_save(self, beauty):
        # 1.把图存下来
        path = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        file_path = './tmp/screenshot/' + path + "/"
        if not os.path.exists(file_path):
            os.mkdir(file_path)
        rq = time.strftime('%Y%m%d%H%M%S-{}'.format(beauty), time.localtime(time.time()))
        screen_name = file_path + rq + '.png'
        shutil.copy('./tmp/screen.png', screen_name)

    # 判断是否满足设定的条件
    def _is_dest(self, face_list, gender = (0, 100), beauty = (0, 100), age = (0, 100)):
        '''
        default:
        gender: (0, 100)
        beauty:(0, 100)
        age:(0, 100)
        '''
        for face in face_list:
            if face['gender'] not in range(gender[0], gender[1] + 1): continue   
            if face['beauty'] not in range(beauty[0], beauty[1] + 1): continue 
            if face['beauty'] not in range(age[0], age[1] + 1): continue
            print("颜值：{}".format(face['beauty']))
            return {'beauty': face['beauty']}
        return False