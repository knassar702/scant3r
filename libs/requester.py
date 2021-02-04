#!/usr/bin/env python3
__name__ = 'ScanT3r'
__author__ = 'Khaled Nassar'
__email__ = 'knassar702@gmail.com'
__version__ = '0.7#Beta'

from requests import get,post,put,packages
from fake_useragent import UserAgent
from requests_toolbelt.utils import dump
import sys

ua = UserAgent(verify_ssl=False,use_cache_server=True)
packages.urllib3.disable_warnings()

class NewRequest:
    def __init__():
        pass
    def Setup(redirect=False,dump=None,cookie=None,header={},timeout=None,proxies=None,random_agents=None):
        global cookies,headers,Dump,Timeout,random_Agents,allow_redirects,proxy
        allow_redirects = redirect
        cookies = cookie
        headers = header
        Dump = dump
        proxy = proxies
        random_Agents = random_agents
        Timeout = timeout
        return {
                'redirect':allow_redirects,
                'cookies':cookies,
                'headers':headers,
                'timeout':Timeout,
                'proxy':proxy,
                'dump':Dump,
                'random_agents':random_Agents
                }
    def Update(redirect=False,dump=None,cookie=None,header={},timeout=None,proxies=None,random_agents=None):
        global allow_redirects,cookies,Dump,Timeout,random_Agents,proxy,headers
        update = {}
        if dump:
            Dump = dump
            update['dump'] = Dump
        if redirect:
            allow_redirects = redirect
            update['redirect'] = redirect
        if cookie:
            cookies = cookie
            update['cookies'] = cookie
        if header:
            headers = header
            update['headers'] = header
        if proxies:
            proxy = proxies
            update['proxy'] = proxies
        if random_agents:
            random_Agents = random_agents
            update['random_agents'] = random_agents
        if timeout:
            Timeout = timeout
            update['timeout'] = timeout
        return update
    def Dump():
        return {
                'redirect':allow_redirects,
                'cookies':cookies,
                'headers':headers,
                'timeout':Timeout,
                'proxy':proxy,
                'dump':Dump,
                'random_agents':random_Agents
                }
    def Get(url):
        try:
            if random_Agents:
                headers['User-agent'] = ua.random
            r = get(url,allow_redirects=allow_redirects,cookies=cookies,headers=headers,timeout=Timeout,proxies=proxy,verify=False)
            if Dump:
                print(dump.dump_all(r).decode('utf-8'))
            return r
        except:
            return 0
    def Post(url,data):
        try:
            if random_Agents:
                headers['User-agent'] = ua.random
            r = post(url,allow_redirects=allow_redirects,cookies=cookies,headers=headers,timeout=Timeout,data=data,proxies=proxy,verify=False)
            if Dump:
                print(dump.dump_all(r).decode())
            return r
        except:
            return 0
    def Put(url,data):
        try:
            if random_Agents:
                headers['User-agent'] = ua.random
            r = put(url,allow_redirects=allow_redirects,cookies=cookies,headers=headers,timeout=Timeout,data=data,proxies=proxy,verify=False)
            if Dump:
                print(dump.dump_all(r).decode())
            return r
        except:
            return 0
