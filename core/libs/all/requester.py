#!/usr/bin/env python3
__author__ = 'Khaled Nassar'
__email__ = 'knassar702@gmail.com'
__version__ = '0.7#Beta'

from requests import Request,Session,request,packages
from .data import post_data,extractHeaders,dump_request,dump_response
from urllib.parse import urlparse
import sys,time,random

packages.urllib3.disable_warnings()



class Agent:
    def __init__(self):
        self.all = ['Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0']
        self.random = random.choice(self.all)
    def load(self):
        with open('wordlists/txt/agents.txt','r') as aw:
            for i in aw:
                if len(i.rstrip()) > 1:
                    self.all.append(i.rstrip())
        self.random = random.choice(self.all)



class http:
    def __init__(self,opts):
        self.timeout = opts['timeout']
        self.headers = opts['headers']
        self.ragent = opts['ragent']
        self.debug = opts['debug']
        self.proxy = opts['proxy']
        self.redirect = opts['redirect']
        self.delay = opts['delay']
        self.count = 0
    def send(self,method='GET',url=None,body={},headers={},redirect=False,org=True):
        try:
            a = Agent()
            if self.ragent:
                a.load()
            if 'User-agent' not in headers.keys():
                headers['User-agent'] = a.random
            if self.headers:
                for h,v in self.headers.items():
                    headers[h] = v
            if self.redirect:
                redirect = True
            else:
                redirect = False
            if self.timeout:
                timeout = self.timeout
            else:
                timeout = 10
            if type(self.proxy) == dict:
                proxy = self.proxy
            else:
                proxy = {}
            if org:
                if body:
                    body = post_data(body)
                else:
                    body = {}
                if method != 'GET':
                    if body:
                        pass
                    else:
                        body = post_data(urlparse(url).query)
                        url = url.split('?')[0]
            time.sleep(self.delay)
            req = request(
                    method,
                    url,
                    data=body,
                    headers=headers,
                    allow_redirects=redirect,
                    verify=False,
                    timeout=timeout,
                    proxies=proxy)
            self.count += 1
            if self.debug:
                print(f'--- [#{self.count}] Request ---')
                print(dump_request(req).decode())
                print('\n---- RESPONSE ----')
                print(dump_response(req).decode())
                print('--------------------\n\n')
            return req
        except Exception as e:
            if self.debug:
                print(e)
            return 0
    def custom(self,method='GET',url=None,body={},headers={},timeout={},redirect=False,proxy={}):
        try:
            time.sleep(self.delay)
            req = Request(method,url,data=body,headers=headers)
            s = Session()
            res = s.send(
                req.prepare(),
                timeout=timeout,
                allow_redirects=redirect,
                verify=False,
                proxies=proxy
            )
            return res
        except Exception as e:
            if self.debug:
                print(f'Error > {e}')
            return 0
