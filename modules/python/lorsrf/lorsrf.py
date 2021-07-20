#!/usr/bin/env python3
__author__ = 'Khaled Nassar'
__email__ = 'knassar702@gmail.com'
__version__ = '0.8#Beta'

from threading import Thread
from queue import Queue
from urllib.parse import urlparse # url parsing
from wordlists import ssrf_parameters # ssrf parameters wordlist
from scan import Scan

q = Queue()


parameters_in_one_request = 10

# parameters_in_one_request = 2

# ?ex1=http://google.com&ex2=http://google.com

class Lorsrf(Scan):
    def __init__(self, opts, http):
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
            if method == 'GET':
                r = self.http.send(method, url)
            else: 
                r = self.http.send(method, url.split('?')[0], body=urlparse(url).query)

    def check_url(self, url: str, par: str, pay: str) -> str:
        if len(urlparse(url).query) > 0:
            return f'&{par}={pay}'
        else:
            return f'?{par}={pay}'
    
    def org(self):
        l = len(ssrf_parameters())
        newurl = self.opts['url']
        allu = []
        for par in ssrf_parameters():
            pay = f"{self.opts['host']}/{par}"
            newurl = self.check_url(newurl, par, pay)
            if len(urlparse(newurl).query.split('=')) == parameters_in_one_request + 1:
                allu.append(newurl)
                newurl = self.opts['url']
        return allu 
        