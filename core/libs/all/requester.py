#!/usr/bin/env python3
__author__ = 'Khaled Nassar'
__email__ = 'knassar702@gmail.com'
__version__ = '0.7#Beta'

from requests import Request, Session, request, packages
from .data import post_data, dump_request, dump_response
from urllib.parse import urlparse
import time, random

packages.urllib3.disable_warnings()

# Create an User Agent 
# Choice one user agent from  the text file agents.txt 
# Another Solution : https://github.com/hellysmile/fake-useragent
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
        
class Http:
    def __init__(self, opts : dict):
        self.timeout = opts['timeout']
        self.headers = opts['headers']
        self.random_agents = opts['random_agents']
        self.debug = opts['debug']
        self.proxy = opts['proxy']
        self.allow_redirects = opts['allow_redirects']
        self.delay = opts['delay']
        self.count = 0
    
    # Send a request 
    def send(self, method='GET', url=None, body={}, headers={}, allow_redirects=False, org=True):
        try:
            # Generate user agent 
            a = Agent()
            if self.random_agents:
                a.load()
            
            # Add user agent to headers 
            if 'User-agent' not in headers.keys():
                headers['User-agent'] = a.random
            
            # set headers     
            if self.headers:
                for h,v in self.headers.items():
                    headers[h] = v
            
            # follow 302 redirects   
            allow_redirects = False
            if self.allow_redirects:
                allow_redirects = True                
            
            # Set timeout
            timeout = 10
            if self.timeout:
                timeout = self.timeout
            
            # set proxy 
            proxy = {}
            if type(self.proxy) == dict:
                proxy = self.proxy
                
            if org:
                body = {}
                if body:
                    body = post_data(body)

                if method != 'GET' and not body:
                    body = post_data(urlparse(url).query)
                    url = url.split('?')[0]
                        
            time.sleep(self.delay)
            req = request(
                    method,
                    url,
                    data=body,
                    headers=headers,
                    allow_redirects=allow_redirects,
                    verify=False,
                    timeout=timeout,
                    proxies=proxy)
            self.count += 1 # number of request
            
            if self.debug: # show request and response (-d option)
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
    # send a request with custom options (without user options)
    def custom(self, method='GET', url=None, body={}, headers={}, timeout={}, allow_redirects=False, proxy={}):
        try:
            time.sleep(self.delay)
            req = Request(method, url, data=body, headers=headers)
            s = Session()
            res = s.send(
                req.prepare(),
                timeout=timeout,
                allow_redirects=allow_redirects,
                verify=False,
                proxies=proxy
            )
            return res
        except Exception as e:
            if self.debug:
                print(f'Error > {e}')
            return 0
