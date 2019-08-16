# -*- coding: utf-8 -*-
'''
create by: 小宝
mail: 1435682155@qq.com
create date: 2019.8.17
Purpose: 程序入口
'''
import sys
import argparse
import signal

VERSION = "1.0.0"

 
def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')

def main():
    if sys.version_info.major != 3:
        exit('Please run under Python3')
    print('程序版本号：{}'.format(VERSION))  
    
    while True:
        try:
            key = input(
                "\n=========***欢迎使用app-bot***=========\n"+
                "请输入序号选择要操作的app：\n"+
                "> 1：soul\n"+
                "> 2：微信\n"+
                "> 0: 退出程序\n"+
                "=======================================\n"
                "请输入[1/2/0]："
            )
            key = int(key)
            if key == 1:
                from app.soul import soul
                return soul().run() 
            elif key == 2:
                from app.wechat import wechat
                return wechat().run()
            elif key == 0:
                exit('谢谢使用')
            else:
                pass
        except ValueError:
            print('按提示输入')
            continue
        except KeyboardInterrupt:
            print('已屏蔽Ctrl+C，输入0退出程序')
            continue
        

if __name__ == '__main__':
    main()

