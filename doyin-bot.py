# -*- coding: utf-8 -*-
import sys
from app.doyin import doyin

if sys.version_info.major != 3:
    exit('Please run under Python3')
    
if __name__ == '__main__':
    obj = doyin()
    obj.run()

