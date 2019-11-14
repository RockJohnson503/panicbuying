# encoding: utf-8

"""
File: demo.py
Author: Rock Johnson
Description: 此文件为案例文件
"""
import sys
sys.path.append('../')
try:
    from panicbuying.panic import Panic
except:
    from panicbuying.panicbuying.panic import Panic

if __name__ == '__main__':
    # browser='Chrome', version='78.0.0'
    xm = Panic(store='小米', url='https://item.mi.com/product/10000164.html')
    xm.start()
    # xm.close()