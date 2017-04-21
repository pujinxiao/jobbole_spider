# -*- coding: utf-8 -*-
__author__ = 'jinxiao'
import hashlib

def get_md5(url):
    '''md5加密'''
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()
