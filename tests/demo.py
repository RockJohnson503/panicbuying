# encoding: utf-8

"""
File: test.py
Author: Rock Johnson
"""
from panicbuying.panicbuying.panic import Panic

if __name__ == '__main__':
    xm = Panic(store='小米', driver='chromedriver-74.exe', account='18223203525', password='k836867547', goods_name='小米手环4', nth=1)
    xm.start()
    # xm.close()