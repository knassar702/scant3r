#!/usr/bin/env python3
__author__ = 'Khaled Nassar'
__email__ = 'knassar702@gmail.com'
__version__ = '0.8#Beta'

from threading import Thread
from queue import Queue
from urllib.parse import urlparse # url parsing
from wordlists import ssrf_parameters # ssrf parameters wordlist
from modules import Scan
from core.libs import Http

q = Queue()


# send requests per sec
parameters_in_one_request = 10

# parameters_in_one_request = 2

# ?ex1=http://google.com&ex2=http://google.com

class Lorsrf(Scan):
    def __init__(self, opts: dict, http: Http):
        super().__init__(opts, http)
    
    def start(self): 
        for _ in range(int(self.opts['threads'])):
            p1 = Thread(target=self.threader)
            p1.daemon = True
            p1.start()
        for url in self.org():
            q.put(url)
        q.join()

    def threader(self):
        while True: 
            url = q.get()
            self.lor(url)
            q.task_done()

    def lor(self, url: str):
        for method in self.opts['methods']:
            self.send_request(method, url)
    def check_url(self, url: str, param: str, payload: str) -> str:
        if len(urlparse(url).query) > 0:
            return f'&{param}={payload}'
        return f'?{param}={payload}'
    
    def org(self) -> list:
        l = len(ssrf_parameters())
        newurl = self.opts['url']
        allu = []
        for par in ssrf_parameters():
            pay = f"{self.opts['host']}/{par}"
            newurl += self.check_url(newurl, par, pay)
            if len(urlparse(newurl).query.split('=')) == parameters_in_one_request + 1:
                allu.append(newurl)
                newurl = self.opts['url']
        return allu 
        
