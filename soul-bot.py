# -*- coding: utf-8 -*-
import sys
from app.soul import soul

if sys.version_info.major != 3:
    exit('Please run under Python3')
    
if __name__ == '__main__':
    obj = soul()
    obj.run()

