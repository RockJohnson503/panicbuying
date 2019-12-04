# encoding: utf-8

"""
File: chrome.py
Author: Rock Johnson
"""
from .browsers import Browser
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Stores:
    def __init__(self, **kwargs):
        self._url = kwargs['url']
        self._addr_nth = kwargs.get('addr_nth') or 1
        self._browser = Browser().get(kwargs.get('browser'), kwargs.get('version'))

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

    def close(self):
        self._browser.quit()


class Xiaomi(Stores):
    def __init__(self, **kwargs):
        Stores.__init__(self, **kwargs)
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


def wait(driver, time, css, desc):
    try:
        element = WebDriverWait(driver, time).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css))
        )
        return element
    except:
        raise SystemError('[%s]元素不存在或选择器未更新,若元素确实存在请联系作者' % desc)
