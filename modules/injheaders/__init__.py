#!/usr/bin/env python3
from yaml import safe_load
from re import findall
from urllib.parse import urlparse
from core.libs import post_data
from wordlists import XSS

class Scan:
    def __init__(self,opts,r):
        self.opts = opts
        self.http = r
        self.blind = list()
        self.conf = safe_load(open('modules/injheaders/payloads.yaml','r'))
        for i in XSS(opts['blindxss']).blind:
            self.conf[i] = [{'text':i},{'regex':False}]
    def start(self,url,methods=['GET']):
        http = self.http
        found = dict()
        headers = safe_load(open('modules/injheaders/headers.yaml','r'))
        for method in methods:
            for payload,matcher in self.conf.items():
                for h,v in headers.copy().items():
                    for payload,matcher in self.conf.copy().items():
                        headers[h] = f'{v}{payload}'
                        try:
                            found[h]
                        except:
                            found[h] = list()
                        try:
                            if method != 'GET':
                                r = http.send(method,url.split('?')[0],headers=headers,body=urlparse(url).query)
                            else:
                                r = http.send(method,url,headers=headers)
                            if r != 0:
                                if matcher[1]['regex']:
                                    c = findall(matcher[0]['text'],r.content.decode('utf-8'))
                                    if c:
                                        print(f'[INJHEADERS] Found :> {h} | {payload} {c}')
                                        found[h].append({payload:[method:f'{h} | {c}']})
                                else:
                                    try:
                                        int(matcher[0]['text'])
                                        if payload in r.content.decode('utf-8'):
                                            print(f'[INJHEADERS] Found :> {h} | {payload}')
                                            found[h].append({payload:[method,h]})
                                    except:
                                        if matcher[0]['text'] in r.content.decode('utf-8'):
                                            print(f'[INJHEADERS] Found :> {h} | {payload} {matcher[0]["text"]}')
                                            found[h].append({payload:{method:[h,matcher[0]['text']]}})
                        finally:
                                headers[h] = v
def main(opts,r):
    s = Scan(opts,r)
    s.start(url=opts['url'],methods=opts['methods'])
