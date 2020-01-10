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


def main():
    '''
    公共参数:
    store: 商城或书店名称(小米|文泉), browser: 浏览器(目前只支持Chrome),
    version: 浏览器版本号, quit: 运行完后是否退出浏览器(默认不退出),
    hidden: 是否启用界面(默认启用),

    商城抢购:
    url: 抢购商城地址, addr_nth: 收货地址(选择第几个收货地址,默认第一个),

    书店扒书(quit默认退出, hidden默认不启用):
    books: {'书名': '电子书链接地址'}, path: 电子书图片保存地址(保存地址文件不存在需要先创建),
    account: 账号, password: 密码,
    '''
    books = {
        '书名': '电子书链接地址',
    }
    xm = Panic(browser='Chrome', version='78.0.0', store='文泉',
               books=books, path='路径', account='账号', password='密码',
               )
    xm.start()


if __name__ == '__main__':
    main()
