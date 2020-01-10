# encoding: utf-8

"""
File: browsers.py
Author: Rock Johnson
"""
import os
import sys
import stat
import shutil
import zipfile
import platform
import urllib.request
from urllib.parse import urljoin

import requests
from selenium import webdriver
from bs4 import BeautifulSoup as bs


class Browser:
    def __init__(self):
        self._browsers = {
            'Chrome': Chrome,
            # 'Opera': Opera,
            # 'Mozilla Firefox': Firefox,
        }

    def get(self, browser=None, version=None, **kwargs):
        res = None
        if browser and not version:
            raise ValueError('使用指定的浏览器必须输入浏览器对应的版本号')
        if browser and self._browsers.get(browser):
            res = self._browsers[browser](version, **kwargs)
        else:
            programs = self._get_program()
            for k, v in self._browsers.items():
                if b := self._find(programs, k):
                    res = v(b, **kwargs)
                    break
        if res:
            try:
                return res.get()
            except:
                res.download()
                return res.get()
        raise SystemError('请先安装以下浏览器:', ', '.join(self._browsers.keys()))

    def _find(self, dt, needle):
        for k, v in dt.items():
            if needle in k:
                return v

    def _get_program(self):
        import winreg
        keys = [winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER]
        sub_key = [r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall',
                   r'SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall']
        soft = {}
        for k in keys:
            for i in sub_key:
                try:
                    key = winreg.OpenKey(k, i, 0, winreg.KEY_ALL_ACCESS)
                except FileNotFoundError:
                    continue
                for j in range(winreg.QueryInfoKey(key)[0] - 1):
                    try:
                        key_path = i + '\\' + winreg.EnumKey(key, j)
                        each_key = winreg.OpenKey(k, key_path, 0, winreg.KEY_ALL_ACCESS)
                        display_name, REG_SZ = winreg.QueryValueEx(each_key, 'DisplayName')
                        display_version, REG_SZ = winreg.QueryValueEx(each_key, 'DisplayVersion')
                        soft[display_name] = display_version
                    except WindowsError:
                        pass
        return soft


class Browsers:
    _driver_name = 0

    def __init__(self, version, **kwargs):
        self._url = f'http://npm.taobao.org/mirrors/{self._driver_name}/'
        self._version = version
        self._bag = os.path.dirname(sys.executable)
        self._hidden = kwargs.get('hidden', False)

    def get(self):
        raise NotImplementedError()

    def download(self):
        try:  # 如果是64位,则尝试下载64位,没有就下载32位
            file = self._download(self._get_suffix())
        except:
            file = self._download(self._get_suffix('32'))
        suc = self._extract(file)
        if suc:
            self._delete(file)

    # 获取下载文件的后缀
    def _get_suffix(self, machine=None):
        system = {
            'Windows': 'win',
            'Linux': 'linux',
            'Mac': 'mac',
        }.get(platform.system(), 'win')
        machine = machine or platform.machine()[-2:]
        return f'{system}{machine}.zip'

    # 获取当前版本的驱动下载路径
    def _version_url(self):
        versions = []
        v = self._version
        html = requests.get(self._url).content
        soup = bs(html, 'html.parser')
        for a in soup.find_all('a'):
            if v[:v.find('.', v.find('.') + 1)] in a.text:
                if a.attrs.get('href'):
                    versions.append(a.attrs['href'])
        if not versions:
            raise SystemError('没有当前版本浏览器的驱动,请升级浏览器至最新版本或下载其它浏览器')
        return sorted(versions)[0]

    # 下载当前版本的驱动压缩包
    def _download(self, suffix):
        base_url = urljoin(self._url, self._version_url())
        html = requests.get(base_url).content
        soup = bs(html, 'html.parser')
        for a in soup.find_all('a'):
            if a.text.endswith(suffix):
                file = a.text
                break
        else:
            raise FileNotFoundError('没有找到符合当前系统的驱动')
        url = urljoin(base_url, file)
        path = os.path.join(self._bag, file)
        urllib.request.urlretrieve(url, path)
        return path

    # 提取下载的zip压缩包
    def _extract(self, file):
        zf = zipfile.ZipFile(file)
        try:
            for z in zf.filelist:
                start = z.filename.rfind('/')
                if self._driver_name in z.filename[0 if start == -1 else start:]:
                    zf.extract(z, self._bag)
                    os.chmod(os.path.join(self._bag, z.filename), stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
            flag = True
        except:
            print('解压失败,请自行解压文件:', file)
            flag = False
        zf.close()
        return flag

    # 删除下载的zip压缩包
    def _delete(self, file):
        os.remove(file)


# 谷歌浏览器
class Chrome(Browsers):
    def __init__(self, version, **kwargs):
        self._driver_name = 'chromedriver'
        super().__init__(version, **kwargs)

    def get(self):
        options = webdriver.ChromeOptions()
        options.add_argument('start-maximized')
        if self._hidden:
            options.add_argument('--headless')
        return webdriver.Chrome(options=options)


# 欧朋浏览器
class Opera(Browsers):
    def __init__(self, version, **kwargs):
        self._driver_name = 'operadriver'
        super().__init__(version, **kwargs)

    def get(self):
        return webdriver.Opera()

    def _delete(self, file):
        os.remove(file)
        extract = os.path.splitext(file)[0]
        if not os.path.isdir(extract):
            return
        for c in os.listdir(extract):
            if self._driver_name in c:
                shutil.copy(os.path.join(extract, c), self._bag)
        shutil.rmtree(extract)


# 火狐浏览器
class Firefox(Browsers):
    def __init__(self, version, **kwargs):
        self._driver_name = 'geckodriver'
        super().__init__(version, **kwargs)

    def get(self):
        options = webdriver.FirefoxOptions()
        options.add_argument('start-maximized')
        return webdriver.Firefox(options=options)
