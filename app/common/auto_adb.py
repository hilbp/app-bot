# -*- coding: utf-8 -*-
import os
import subprocess
import platform
import random


class auto_adb():
    def __init__(self):
        try:
            adb_path = 'adb'
            subprocess.Popen([adb_path], stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
            self.adb_path = adb_path
        except OSError:
            if platform.system() == 'Windows':
                adb_path = os.path.join('Tools', "adb", 'adb.exe')
                try:
                    subprocess.Popen(
                        [adb_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    self.adb_path = adb_path
                except OSError:
                    pass
            else:
                try:
                    subprocess.Popen(
                        [adb_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                except OSError:
                    pass
            print('请安装 ADB 及驱动并配置环境变量')
            exit(1)
    
    def run(self, raw_command):
        # print(raw_command)
        command = '{} {}'.format(self.adb_path, raw_command)
        process = os.popen(command)
        output = process.read()
        return output

    def get_screen(self):
        cmd = 'shell wm size'
        return self.run(cmd)

    def test_device(self):
        print('检查设备是否连接...')
        command_list = [self.adb_path, 'devices']
        process = subprocess.Popen(command_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = process.communicate()
        if output[0].decode('utf8') == 'List of devices attached\n\n':
            print('未找到设备')
            print('adb 输出:')
            for each in output:
                print(each.decode('utf8'))
            exit(1)
        print('设备已连接')
        print('adb 输出:')
        for each in output:
            print(each.decode('utf8'))

    def test_density(self):
        cmd = 'shell wm density'
        return self.run(cmd)

    def test_device_detail(self):
        cmd = 'shell getprop ro.product.device'
        return self.run(cmd)

    def test_device_os(self):
        cmd = 'shell getprop ro.build.version.release'
        return self.run(cmd)

        
