#!/usr/bin/env python3
import random
from core.libs import insert_to_params,random_str,post_data,urlencoder,insert_to_params_urls
from urllib.parse import urlparse
from wordlists import XSS


class Scan:
    def __init__(self,opts,r):
        self.http = r
        self.opts = opts
        self.payloads = XSS(opts['blindxss'])
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
    def headers(self,url,methods=['GET','POST'],headers={'User-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}):
        http = self.http
        header = headers.copy()
        for payload in self.payloads.blind:
            for h,v in headers.items():
                header[h] = v + payload
            print(payload)
#        for met in methods:
#            http.send(met,url,headers=headers)
    def start(self,url,methods=['GET','POST']):
        self.bugs = []
        for i in methods:
            self.ref = []
            txt = f'scan{random_str(3)}tr'
            n = insert_to_params_urls(url,txt)
            for wp in n:
                if i != 'GET':
                    r = self.http.send(i,wp.split('?')[0],body=urlparse(wp).query,headers=headers)
                    if txt in r.content.decode('utf-8'):
                        self.ref.append(wp)
                else:
                    r = self.http.send(i,wp,headers=headers)
                    if txt in r.content.decode('utf-8'):
                        self.ref.append(wp)
            for rp in self.ref:
                for P in self.payloads.payloads:
                    nurl = rp.replace(txt,P)
                    if i == 'GET':
                        r = self.http.send(i,nurl)
                    else:
                        r = self.http.send(i,nurl.split('?')[0],body=urlparse(nurl).query)
                    if P in r.content.decode('utf-8'):
                        print(f'[XSS] Found :> {nurl.split("?")[0]}\n\t[!] Method: {i}\n\t[!] Params: {urlparse(nurl).query}')
                        self.bugs.append({
                                'Bug':'XSS',
                                'url':nurl.split('?')[0],
                                'method':i,
                                'params':urlparse(nurl).query
                                })
                        break
        return self.bugs

def main(opts,r):
    scanner = Scan(opts,r)
    scanner.start(opts['url'])
