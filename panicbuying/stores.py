# encoding: utf-8

"""
File: chrome.py
Author: Rock Johnson
"""
import os, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Stores:
    def __init__(self, **kwargs):
        self._account = kwargs['account']
        self._password = kwargs['password']
        self._goods_name = kwargs['goods_name']
        self._goods_nth = kwargs['goods_nth']
        self._addr_nth = kwargs['addr_nth']

        try:
            os.uname()
            mark = '/'
        except:
            mark = '\\'
        self._exec_path = os.path.abspath(__file__).replace('stores.py', 'drivers%s%s' % (mark, kwargs['driver']))
        self._options = webdriver.ChromeOptions()
        self._options.add_argument('start-maximized')

    def _login(self):
        # 登录
        pass

    def _choice_goods(self):
        # 选择物品
        pass

    def _start_panic(self):
        # 开始抢购
        pass

    def start(self):
        self._brower = webdriver.Chrome(self._exec_path, options=self._options)
        self._brower.get(self._url)
        self._login()
        self._choice_goods()
        self._start_panic()

    def close(self):
        self._brower.quit()


class Xiaomi(Stores):
    def __init__(self, **kwargs):
        Stores.__init__(self, **kwargs)
        self._url = 'https://www.mi.com'

    def _login(self):
        # 登录
        index_login_btn = wait(self._brower, 10, '#J_userInfo a.link:nth-child(1)')
        if index_login_btn:
            index_login_btn.click()  # 点击登录按钮

        agree_modal = wait(self._brower, 5, '#J_agreeModal')
        time.sleep(1)
        if agree_modal and agree_modal.is_displayed():
            primary_btn = self._brower.find_element_by_css_selector('.btn-primary.J_sure')
            primary_btn.click() # 点击同意按钮

        # 输入账号
        account_input = wait(self._brower, 10, '#username')
        password_input = wait(self._brower, 10, '#pwd')

        account_input.send_keys(self._account)
        password_input.send_keys(self._password)
        password_input.send_keys(Keys.ENTER)

        ok = wait(self._brower, 10, '#J_userInfo span.user')
        if not ok:
            self._login()

    def _choice_goods(self):
        # 选择要抢购的商品
        search_input = self._brower.find_element_by_css_selector('#search')
        search_input.send_keys(self._goods_name)
        search_input.send_keys(Keys.ENTER)

        goods_item = wait(self._brower, 10, '.goods-list-box .goods-item:nth-child(%d)' % self._goods_nth)
        if goods_item:
            goods_item.click()
        buy_btn = wait(self._brower, 10, '#J_headNav .btn-primary')
        if buy_btn:
            buy_btn.click()

        wait(self._brower, 10, '#J_buyBtnBox li:nth-child(1)')

    def _start_panic(self):
        # 开始抢购
        flag = 0
        while True:
            try:
                flag = 0
                buy_btn = self._brower.find_element_by_css_selector('#J_buyBtnBox li:nth-child(1)')
                flag = 1
                buy_btn.click()
            except:
                if flag == 0:
                    break
                elif flag == 1:
                    print('无法点击按钮')
        print('正在排队, 请等待结果')
        ok = wait(self._brower, 200, '#J_goodsBox')
        if ok:
            shop_btn = wait(self._brower, 10, '.actions.J_actBox a.btn-primary')
            if shop_btn:
                shop_btn.click()
            pay_btn = wait(self._brower, 10, '#J_goCheckout')
            if pay_btn:
                pay_btn.click()
            address = wait(self._brower, 10, '#J_addressList div:nth-child(%d)' % self._addr_nth)
            if address:
                address.click()
            order_btn = wait(self._brower, 10, '#J_checkoutToPay')
            if order_btn:
                order_btn.click()
            print('抢购成功,请尽快付款!')
        else:
            print('抢购失败!')


def wait(driver, time, css):
    try:
        element = WebDriverWait(driver, time).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css))
        )
        return element
    except:
        return False