#!/usr/bin/env python3
__author__ = 'Khaled Nassar'
__email__ = 'knassar702@gmail.com'
__version__ = '0.8#Beta'

from urllib.parse import urlparse # url parsing
from logging import getLogger
from wordlists import ssrf_parameters # ssrf parameters wordlist
from core.libs import OOB , alert_bug , post_data , Http 
from urllib.parse import urlparse
from modules import Scan
from modules.python.xss import main as xss_main
from modules.python.xss_param import main as xss_param_main
from modules.python.sqli import main as sqli_main
from modules.python.ssrf import main as ssrf_main
from modules.python.ssti import main as ssti_main
from queue import Queue
from threading import Thread

log = getLogger('scant3r')

# send requests per sec
parameters_in_one_request = 10

# ?ex1=http://google.com&ex2=http://google.com

class Lorsrf(Scan):
    def __init__(self, opts: dict, http: Http):
        self.oob_host = OOB(http)
        self.host = self.oob_host.new()
        self.queue = Queue()
        super().__init__(opts, http)
    
    def guess(self):
        urls = []
        for url in self.make_params():
            urls.append(url)
        for url in urls:
            self.queue.put(url)

        log.debug(f'Started on {self.opts["url"]} with 10 parameters per secound ({self.opts["methods"]})')
        self.queue.join()
    
    def threader(self):
        while True:
            item = self.queue.get()
            self.sender(item)
            self.queue.task_done()

    def start(self):
        thread = Thread(target=self.threader)
        thread.daemon = True
        thread.start()
        self.guess()

    def sender(self, url: str,body : dict = {}):
        for method in self.opts['methods']:
            req = self.send_request(method, url)
            if type(req) != list:
                op = self.opts.copy()
                op['url'] = url
                op['method'] = method
                if self.opts.get('host'):
                    pass
                else:
                    if self.oob_host.poll():
                        alert_bug('Lorsrf -> New Request',req,host=self.host,results=f'$ curl -H "Authorization: Secret {self.oob_host.key}" https://odiss.eu:1337/events -sk | jq')
                if self.opts['more_scan'] == True:
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
    
    def make_params(self) -> list:
        parameters_lenght = len(ssrf_parameters())
        newurl = self.opts['url']
        all_urls = []
        protocols = ['http://','https://','']
        for parameter in ssrf_parameters():
            for protocol in protocols:
                if self.opts.get('host'):
                    new_host = self.opts.get('host').replace("%PARAM%",parameter).replace('%HOST%',urlparse(newurl).netloc).replace("%PATH%",urlparse(newurl).path).replace("%PORT%",str(urlparse(newurl).port))
                else:
                    new_host = f"{protocol}{parameter}.{self.host}"
                newurl += self.check_url(newurl, parameter, new_host)
                if len(urlparse(newurl).query.split('=')) == parameters_in_one_request + 1:
                    all_urls.append(newurl)
                    newurl = self.opts['url']
        return all_urls 
        
