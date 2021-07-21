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
            r = self.http.send(method,url)
            if r != 0 and r.status_code != 405:
                method_allowed[method] = {url: r.status_code}
        return method_allowed
    
    def start(self):
        self.bugs = []
        for i in self.opts['methods']:
            self.ref = []
            txt = f'scan{random_str(3)}tr'
            n = remove_dups_urls(insert_to_params_urls(self.opts['url'],txt))
            for wp in n:
                if i == 'GET':
                    r = self.http.send(i,wp)
                    if r != 0 and txt in r.text:
                        self.ref.append(wp)
                else:                
                    r = self.http.send(i,wp.split('?')[0],body=urlparse(wp).query)
                    if r != 0 and txt in r.text:
                        self.ref.append(wp)
            for rp in self.ref:
                for P in self.payloads:
                    P = P.rstrip() # remove new lines from payloads 
                    nurl = rp.replace(txt,P)
                    if i == 'GET':
                        r = self.http.send(i,nurl)
                    else:
                        r = self.http.send(i,nurl.split('?')[0],body=urlparse(nurl).query)
                    if r != 0 and P in r.text:
                        self.bugs.append({
                            'params':urlparse(nurl).query,
                            'payload':P,
                            'http':r
                            })
                        break
        self.fbug = []
        for bu in self.bugs:
            self.fbug.append(alert_bug('XSS',**bu))
        return self.fbug

