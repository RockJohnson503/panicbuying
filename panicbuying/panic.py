# encoding: utf-8

"""
File: panic.py
Author: Rock Johnson
"""
from .stores import Xiaomi


class Panic:
    def __init__(self, **kwargs):
        stores = {
            '小米': Xiaomi,
        }

        if stores.get(kwargs['store']):
            self._store = stores[kwargs['store']](**kwargs)
        else:
            raise KeyError('暂不支持%s商城的抢购' % kwargs['store'])

    def start(self):
        self._store.start()

    def close(self):
        self._store.close()