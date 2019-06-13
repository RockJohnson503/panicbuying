# encoding: utf-8

"""
File: demo.py
Author: Rock Johnson
Description: 此文件为案例文件
"""
try:
    # windows
    from panicbuying.panicbuying.panic import Panic
except:
    # linux
    from panicbuying.panic import Panic

if __name__ == '__main__':
    xm = Panic(store='小米', driver='chromedriver', account='你的账户', password='你的密码', goods_name='你需要抢购的商品', nth=1)
    xm.start()
    # xm.close()