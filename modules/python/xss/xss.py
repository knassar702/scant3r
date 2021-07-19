#!/usr/bin/env python3
import random
from core.libs import insert_to_params,remove_dups_urls,random_str,alert_bug,post_data,urlencoder,insert_to_params_urls
from urllib.parse import urlparse
from wordlists import XSS


class Scan:
    def __init__(self,opts,r):
        self.http = r
        self.opts = opts
        self.payloads = XSS(opts['blindxss']).payloads
    def check_method(self,methods,url):
        self.method_allowed = {}
        if self.method_allowed:
            self.method_allowed.clear()
        for u in methods:
            self.method_allowed[u] = {}
        for method in methods:
            r = self.http.send(method,url)
            if r != 0:
                if r.status_code != 405:
                    self.method_allowed[method] = {url:r.status_code}
        return self.method_allowed
    def start(self,url,methods=['GET','POST']):
        self.bugs = []
        for i in methods:
            self.ref = []
            txt = f'scan{random_str(3)}tr'
            n = remove_dups_urls(insert_to_params_urls(url,txt))
            for wp in n:
                if i != 'GET':
                    r = self.http.send(i,wp.split('?')[0],body=urlparse(wp).query)
                    if r != 0:
                        if txt in r.text:
                            self.ref.append(wp)
                else:
                    r = self.http.send(i,wp)
                    if r != 0:
                        if txt in r.text:
                            self.ref.append(wp)
            for rp in self.ref:
                for P in self.payloads:
                    P = P.rstrip() # remove new lines from payloads 
                    nurl = rp.replace(txt,P)
                    if i == 'GET':
                        r = self.http.send(i,nurl)
                    else:
                        r = self.http.send(i,nurl.split('?')[0],body=urlparse(nurl).query)
                    if r != 0:
                        if P in r.text:
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

