#!/usr/bin/env python3

from libs import NewRequest as nq 
from libs import post_data
from libs import insertAfter as inf
from urllib.parse import urlparse
from random import randint

class methods:
    def __init__():
        pass
    def Get(url):
        try:
            if nq.Get(url).status_code != 405:
                return 1
            else:
                return 0
        except:
            return 0
    def Post(url,data=None):
        try:
            if nq.Post(url.split('?')[0],post_data(urlparse(url).query)).status_code != 405:
                return 1
            else:
                return 0
        except:
            return 0
    def Put(url,data=None):
        try:
            if nq.Put(url.split('?')[0],post_data(urlparse(url).query)).status_code != 405:
                return 1
            else:
                return 0
        except:
            return 0

class refxss:
    def __init__():
        pass
    def Get(url):
        try:
            r = nq.Get(inf(url,'=',f'scantrrr'))
            if r.content.decode().lower().find('scantrrr') != -1:
                return 1
            else:
                return 0
        except:
            return 0
    def Post(url):
        try:
            r = nq.Post(url.split('?')[0],post_data(inf(urlparse(url).query,'=','scantrrr')))
            if r.content.decode().lower().find('scantrrr') != -1:
                return 1
            else:
                return 0
        except:
            return 0
    def Put(url):
        try:
            r = nq.Put(url.split('?')[0],post_data(inf(urlparse(url).query,'=','scantrrr')))
            if r.content.decode().lower().find('scantrrr') != -1:
                return 1
            else:
                return 0
        except:
            return 0

class refcrlf:
    def __init__():
        pass
    def Get(url):
        try:
            r = nq.Get(inf(url,'=',f'scantrrr'))
            for header,value in r.headers.items():
                if 'scantrrr' in header or 'scantrrr' in value:
                    return 1
            else:
                return 0
        except:
            return 0
    def Post(url):
        try:
            r = nq.Post(url.split('?')[0],post_data(inf(urlparse(url).query,'=','scantrrr')))
            for header,value in r.headers.items():
                if 'scantrrr' in header or 'scantrrr' in value:
                    return 1
            else:
                return 0
        except:
            return 0
    def Put(url):
        try:
            r = nq.Put(url.split('?')[0],post_data(inf(urlparse(url).query,'=','scantrrr')))
            for header,value in r.headers.items():
                if 'scantrrr' in header or 'scantrrr' in value:
                    return 1
            else:
                return 0
        except:
            return 0
