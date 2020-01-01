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
    # browser='Chrome', version='78.0.0', book='这是一本书名(仅文泉)',
    # path='这是图片保存路径(仅文泉)', account='这是账号(仅文泉)', password='这是密码(仅文泉)'
    xm = Panic(browser='Chrome', version='78.0.0', store='文泉', url='https://wqbook.wqxuetang.com/read/pdf/2033158')
    xm.start()
    # xm.close()