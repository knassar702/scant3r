#!/usr/bin/env python3
__author__ = 'Khaled Nassar'
__email__ = 'knassar702@gmail.com'
__version__ = '0.8#Beta'

import time
import random
import logging
import json
from typing import Union
from requests import Request, Session, request, packages
from requests.models import Response
from .data import post_data, dump_request, dump_response

# ignore ssl warning messages
packages.urllib3.disable_warnings()

# scant3r logger
log = logging.getLogger('rich')

# Create an User Agent
# Choice one user agent from  the text file agents.txt
# Another Solution : https://github.com/hellysmile/fake-useragent


class Agent:
    def __init__(self):
        self.all = ['Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0']
        self.random = random.choice(self.all)

    def load(self):
        try:
            log.debug('loading agents.txt file')
            with open('wordlists/txt/agents.txt', 'r') as aw:
                for i in aw:
                    if len(i.rstrip()) > 1:
                        self.all.append(i.rstrip())
            log.debug('random choice of user agents')
            self.random = random.choice(self.all)
        except Exception as e:
            log.error(e)
            return


class Http:
    def __init__(self, opts: dict):
        self.timeout = opts['timeout']
        self.headers = opts['headers']
        self.cookies = opts['cookies']
        self.random_agents = opts['random_agents']
        self.debug = opts['debug']
        self.proxy: dict = opts['proxy']
        self.allow_redirects: bool = opts['allow_redirects']
        self.delay = opts['delay']
        self.json : bool = opts['json']

    # Send a request
    def send(self,
             method: str = 'GET',
             url: Union[str, None] = None,
             body: dict = {},
             headers: dict = {},
             allow_redirects: bool = False,
             org: bool = True,
             files: Union[dict, None] = None,
             timeout: int = 10,
             ignore_errors: bool = False,
             json=False) -> Response:
        try:
            # Generate user agent
            user_agents = Agent()
            if self.random_agents:
                user_agents.load()

            # Add user agent to headers
            if 'User-agent' not in headers.keys():
                headers['User-agent'] = user_agents.random

            # set headers
            if self.headers:
                for header, value in self.headers.items():
                    if not self.cookies and 'Cookie' in header:
                        headers[header] = value

            # Specify cookie
            cookies = {}
            if self.cookies:
                cookies = self.cookies

            # follow 302 redirects
            allow_redirects = False
            if self.allow_redirects:
                allow_redirects = True

            # Set timeout
            if timeout == 10 and self.timeout:
                timeout = self.timeout

            # set proxy
            proxy = {}
            if type(self.proxy) is dict:
                proxy = self.proxy

            # convert body to parameters
            if org:
                if type(body) is str:
                    log.debug(f'convert {body} to dict')
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
                if not json:
                    json = self.json
                if json:
                    json = body
                    body = None
                else:
                    json = None
            else:
                json = None 

            req = request(
                method,
                url,
                data=body,
                headers=headers,
                cookies=cookies,
                files=files,
                allow_redirects=allow_redirects,
                verify=False,
                timeout=timeout,
                proxies=proxy,
                json=json
            )

            if self.delay > 0:
                log.debug(f'sleep {self.delay}')
                time.sleep(self.delay)

            log.debug(dump_request(req))
            log.debug(dump_response(req))
            req.encoding = req.apparent_encoding

            return req
        except Exception as e:
            if ignore_errors is False:
                log.error(e)
            return [0, e]

    # send a request with custom options (without user options)
    def custom(self,
               method='GET',
               url=None,
               body={},
               headers={},
               timeout=10,
               allow_redirects=False,
               proxy={}):
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
            log.exception(e)
            return [0, e]
