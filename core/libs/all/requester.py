#!/usr/bin/env python3
__author__ = 'Khaled Nassar'
__email__ = 'knassar702@gmail.com'
__version__ = '0.8#Beta'

from typing import Union
from requests import Request, Session, request, packages
from requests.models import Response
from .data import post_data, dump_request, dump_response
from urllib.parse import urlparse
import time, random, logging , json

packages.urllib3.disable_warnings() # ignore ssl warning messages

log = logging.getLogger('scant3r') # scant3r logger

# Create an User Agent 
# Choice one user agent from  the text file agents.txt 
# Another Solution : https://github.com/hellysmile/fake-useragent
class Agent:
    def __init__(self):
        self.all = ['Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0']
        self.random = random.choice(self.all)
    def load(self):
        try:
            with open('wordlists/txt/agents.txt','r') as aw:
                for i in aw:
                    if len(i.rstrip()) > 1:
                        self.all.append(i.rstrip())
            self.random = random.choice(self.all)
        except Exception as e:
            log.error(e)
            return

class Http:
    def __init__(self, opts : dict):
        self.timeout: int = opts['timeout']
        self.headers: dict = opts['headers']
        self.cookies: dict = opts['cookies']
        self.random_agents: list = opts['random_agents']
        self.proxy: dict = opts['proxy']
        self.allow_redirects: bool = opts['allow_redirects']
        self.json: bool = opts['json']
        self.delay: int = opts['delay']
        self.count: int = 0
        
    # Send a request 
    def send(self, method: str = 'GET', url: Union[str, None] = None, body: dict = {}, headers: dict = {}, allow_redirects: bool = False, org: bool = False, timeout:int = 10, IgnoreErrors: bool = False, json=None) -> Response:
        try: 
            # Generate user agent
            user_agents = Agent()
            if self.random_agents:
                user_agents.load()

            # Add user agent to headers 
            if 'User-agent' not in headers.keys():
                headers['User-agent'] = user_agents.random

            # set headers     
            if self.headers :
                for h,v in self.headers.items():
                    if not self.cookies and 'Cookie' in h:
                        headers[h] = v
            
            # Specify cookie
            cookies = {}
            if self.cookies:
                cookies = self.cookies

            # follow 302 redirects   
            allow_redirects = False
            if self.allow_redirects:
                allow_redirects = True

            # Set timeout
            if timeout == 10:
                if self.timeout:
                    timeout = self.timeout
            # set proxy
            proxy = {}
            if type(self.proxy) == dict:
                proxy = self.proxy
                
            # convert body to parameters
            if org:
                if body:
                    log.debug('convert body to dict')
                    if type(body) == str:
                            if body.startswith('?'):
                                pass
                            else:
                                body = '?' + body
                            body = post_data(body)
                if method != 'GET' and not body:
                    log.debug('convert body to dict')
                    body = post_data(url)
                    url = url.split('?')[0]
            if method.upper() != 'GET':
                if self.json:
                    if json:
                        json.update(post_data(body))
                    elif type(body) == dict:
                        json = body
                    else:
                        json = post_data(str(body))
                    body = {}
            req = request(method, url, data=body, headers=headers, cookies=cookies, allow_redirects=allow_redirects, verify=False, timeout=timeout, proxies=proxy,json=json)
            if self.delay > 0:
                log.debug(f'sleep {self.delay}')
                time.sleep(self.delay)
                
            self.count += 1 # number of request
            req.encoding = req.apparent_encoding
            
            # show request and response (-d option)
                
            return req
        except Exception as e:
            if IgnoreErrors == False:
                log.error(e)
            return [0,e]
        
    # send a request with custom options (without user options)
    def custom(self, method='GET', url=None, body={}, headers={}, timeout=10, allow_redirects=False, proxy={},json=None):
        try:
            if method.upper() != 'GET':
                if self.json:
                    if json:
                        json.update(post_data(body))
                    elif type(body) == dict:
                        json = body
                    else:
                        json = post_data(str(body))

            time.sleep(self.delay)
            req = Request(method, url, data=body, headers=headers,json=json)
            s = Session()
            res = s.send(
                req.prepare(),
                timeout=timeout,
                allow_redirects=allow_redirects,
                verify=False,
                proxies=proxy,
            )
            return res
        except Exception as e:
            log.error(e)
            return [0,e]
