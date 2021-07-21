#!/usr/bin/env python3
from core.libs import remove_dups_urls, random_str, alert_bug, insert_to_params_urls, Http
from urllib.parse import urlparse
from wordlists import XSS
from logging import getLogger
from modules import Scan

log = getLogger('scant3r')

class Xss(Scan):
    def __init__(self, opts: dict, http: Http):
        super().__init__(opts, http)
        log.info('hi')
        self.payloads = XSS(opts['blindxss']).payloads
        
    def check_method(self, methods: list, url: str) -> dict:
        method_allowed = dict()
        for method in methods:
            method_allowed[method] = {}
            response = self.http.send(method,url)
            if response != 0 and response.status_code != 405:
                method_allowed[method] = {url: response.status_code}
        return method_allowed
    
    def start(self):
        bugs = []
        for method in self.opts['methods']:
            
            ref: list = []
            txt = f'scan{random_str(3)}tr'
            list_url = remove_dups_urls(insert_to_params_urls(self.opts['url'],txt))
            for url in list_url:
                response = self.send_request(method, url)
                if response != 0 and txt in response.text:
                    ref.append(url)
                    
            for rp in ref:
                for P in self.payloads:
                    # remove new lines from payloads
                    P = P.rstrip()  
                    nurl = rp.replace(txt,P)
                    response = self.send_request(method, nurl)
                    if response != 0 and P in response.text:
                        bugs.append({
                            'params':urlparse(nurl).query,
                            'payload':P,
                            'http': response
                        })
                        break
                    
        result_list = []
        for bug in bugs:             
            result_list.append(alert_bug('XSS',**bug))
        
        return result_list

