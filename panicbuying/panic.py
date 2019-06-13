# encoding: utf-8

"""
File: panic.py
Author: Rock Johnson
"""
from .stores import *


class Panic:
    def __init__(self, **kwargs):
        if kwargs['store'] == '小米':
            self._store = Xiaomi(**kwargs)
        else:
            raise KeyError('暂不支持抢购 %s 商城' % kwargs['store'])

    def start(self):
        self._store.start()

    def close(self):
        self._store.close()