# encoding: utf-8

"""
File: chrome.py
Author: Rock Johnson
"""
import os
import time
from urllib import request

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .browsers import Browser


class Stores:
    def __init__(self, **kwargs):
        self._url = kwargs.get('url')
        self._addr_nth = kwargs.get('addr_nth', 1)
        self._quit = kwargs.get('quit', False)
        self._browser = Browser().get(
            kwargs.get('browser'), kwargs.get('version'),
            hidden=kwargs.get('hidden')
        )

    # 登录
    def _login(self):
        pass

    # 选择物品
    def _choice_goods(self):
        pass

    # 开始抢购
    def _start_panic(self):
        pass

    def start(self):
        self._browser.get(self._url)
        self._login()
        self._start_panic()
        if self._quit:
            self.close()

    def close(self):
        self._browser.quit()


class Xiaomi(Stores):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self._url or 'mi.com' not in self._url:
            raise ValueError('您输入的商品路径不属于小米商城')

    # 登录
    def _login(self):
        self._browser.execute_script('var q=document.documentElement.scrollTop=0')
        wait(self._browser, 10, '#J_userInfo a.link:nth-child(1)', '登录').click()
        wait(self._browser, 5, '#J_agreeModal .btn-primary', '同意按钮').click()
        wait(self._browser, 5, '#nav-tabs a[data-tab="qr"]', '扫码登录').send_keys(Keys.ENTER)

        while True:
            try:
                wait(self._browser, 10, '#J_userInfo span.user', '登录成功')
                break
            except:
                pass
        print('登录成功')

    # 选择要抢购的商品
    def _choice_goods(self):
        search_input = self._browser.find_element_by_css_selector('#search')
        search_input.send_keys(self._goods_name)
        search_input.send_keys(Keys.ENTER)

        goods_item = wait(self._browser, 10, '.goods-list-box .goods-item:nth-child(%d)' % self._goods_nth)
        if goods_item:
            goods_item.click()

        windows = self._browser.window_handles
        self._browser.switch_to.window(windows[1])

        buy_btn = wait(self._browser, 10, '#J_headNav .right .btn-primary')
        if buy_btn:
            buy_btn.click()
        wait(self._browser, 10, '#J_buyBtnBox li:nth-child(1)')

    # 开始抢购
    def _start_panic(self):
        flag = 0
        while True:
            try:
                flag = 0
                buy_btn = self._browser.find_element_by_css_selector('#J_buyBtnBox li:nth-child(1)')
                flag = 1
                buy_btn.click()
            except:
                if flag == 0:
                    break
                elif flag == 1:
                    print('无法点击按钮')
        print('正在排队, 请等待结果')
        try:
            wait(self._browser, 200, '#J_goodsBox', '')
        except:
            print('抢购失败!')
        wait(self._browser, 10, '.actions.J_actBox a.btn-primary', '去购物车结算按钮').click()
        wait(self._browser, 10, '#J_goCheckout', '去结算按钮').click()
        wait(self._browser, 10, '#J_addressList > div:nth-child(%d)' % self._addr_nth, '收货地址选项').click()
        wait(self._browser, 10, '#J_checkoutToPay', '去结算按钮').click()
        print('抢购成功,请尽快付款!')


class WenQuan(Stores):
    def __init__(self, **kwargs):
        kwargs['hidden'] = kwargs.get('hidden', True)
        kwargs['quit'] = kwargs.get('quit', True)
        super().__init__(**kwargs)
        self._path = kwargs['path']
        self._account = kwargs['account']
        self._password = kwargs['password']
        self._book = list(kwargs['books'].keys())
        self._url = list(kwargs['books'].values())

    def _login(self):
        wait(self._browser, 5, '.head-box .head-logon', '登录', 'click')
        time.sleep(1)
        wait(self._browser, 5, '#mobilelogin-form-link', '账号密码登录按钮', 'click')
        time.sleep(1)
        wait(self._browser, 5, '#account', '账号输入框').send_keys(self._account)
        wait(self._browser, 5, '#password', '账号输入框').send_keys(self._password)
        wait(self._browser, 5, '#mobilelogin-form > div:nth-child(3) > div > div > input', '登录按钮', 'click')

        while True:
            try:
                wait(self._browser, 10, '.head-logon span', '登录成功')
                break
            except:
                pass
        print("登录成功")

    def _download(self, idx=0):
        book = self._book[idx]
        wait(self._browser, 5, '#pagebox .page-img-box[index="3"]', '书籍')
        pages = self._browser.find_elements_by_css_selector('#pagebox .page-img-box[index]')
        for i, page in enumerate(pages):
            self._browser.execute_script('arguments[0].scrollIntoView();', page)
            time.sleep(0.5)
            img = page.find_element_by_css_selector('img.page-img').get_attribute('src')
            request.urlretrieve(img, os.path.join(self._path, f'{book}-{i}.png'))
            print(f'《{book}》 第{i}页下载完成')
        if len(self._book) - idx > 1:
            self._browser.get(self._url[idx + 1])
            self._download(idx + 1)

    def start(self):
        self._browser.get(self._url[0])
        self._login()
        self._download()
        if self._quit:
            self.close()


def wait(driver, time, css, desc, operate='wait'):
    try:
        element = WebDriverWait(driver, time).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css))
        )
        if operate == 'click':
            driver.execute_script("arguments[0].click();", element)
        return element
    except:
        raise SystemError(f'[{desc}]元素不存在或选择器未更新,若元素确实存在请联系作者')
