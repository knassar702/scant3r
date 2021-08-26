#!/usr/bin/env python3
__author__ = 'Khaled Nassar'
__email__ = 'knassar702@gmail.com'
__version__ = '0.8#Beta'

from threading import Thread
from queue import Queue
from urllib.parse import urlparse # url parsing
from logging import getLogger
from wordlists import ssrf_parameters # ssrf parameters wordlist
from core.libs import alert_bug
from modules import Scan
from modules.python.xss import main as xss_main
from modules.python.xss_param import main as xss_param_main
from modules.python.sqli import main as sqli_main
from modules.python.ssrf import main as ssrf_main
from modules.python.ssti import main as ssti_main
from core.libs import Http

q = Queue()
log = getLogger('scant3r')

# send requests per sec
parameters_in_one_request = 10

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
        log.info(f'Started on {self.opts["url"]} with 10 parameters per secound ({self.opts["methods"]})')
        q.join()

    def threader(self):
        while True: 
            url = q.get()
            self.lor(url)
            q.task_done()

    def lor(self, url: str):
        for method in self.opts['methods']:
            req = self.send_request(method, url)
            if type(req) != list:
                op = self.opts.copy()
                op['url'] = url
                op['method'] = method
                if self.opts['one_scan'] == False:
                    log.debug('Scannig with another modules')
                    xss_main(op,self.http)
                    xss_param_main(op,self.http)
                    ssrf_main(op,self.http)
                    ssti_main(op,self.http)
                    sqli_main(op,self.http)
    def check_url(self, url: str, param: str, payload: str) -> str:
        if len(urlparse(url).query) > 0:
            return f'&{param}={payload}'
        return f'?{param}={payload}'
    
    def org(self) -> list:
        l = len(ssrf_parameters())
        newurl = self.opts['url']
        allu = []
        proto = ['http://','https://','smpt://','']
        if self.opts['host']:
            pass
        else:
            return
        for par in ssrf_parameters():
            for pr in proto:
                pay = f"{pr}{par}.{self.opts['host']}"
                newurl += self.check_url(newurl, par, pay)
                if len(urlparse(newurl).query.split('=')) == parameters_in_one_request + 1:
                    allu.append(newurl)
                    newurl = self.opts['url']
        return allu 
        
