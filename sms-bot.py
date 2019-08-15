# -*- coding: utf-8 -*-
import sys
import argparse
import signal

from app.sms import sms

VERSION = "1.0.0"
obj = sms()


if __name__ == '__main__':
    obj.run()

