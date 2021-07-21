#!/usr/bin/env python3
from yaml import safe_load
from urllib.parse import urlparse
from core.libs import alert_bug, dump_response, Http
from wordlists import XSS
import re
from modules import Scan

class Injheaders(Scan):
    def __init__(self, opts: dict, http: Http):
        super().__init__(opts, http) 
        self.conf = self.define_conf()
        
    def define_conf(self):
        conf = self.open_yaml_file("injheaders/payloads.yaml")
        for i in XSS(self.opts['blindxss']).blind:
            conf[i] = [{'text':i},{'regex':False}]
        return conf
                    
    def start(self): 
        headers = self.open_yaml_file('injheaders/headers.yaml')
        for method in self.opts['methods']:
            for payload, matcher in self.conf.items(): 
                for h, v in headers.copy().items(): 
                    headers[h] = f'{v}{payload}'
                    try: 
                        if method != 'GET':
                            response = self.http.send(method, self.opts['url'].split('?')[0],headers=headers, body=urlparse(self.opts['url']).query)
                        else:
                            response = self.http.send(method, self.opts['url'], headers=headers)
                            
                        if response != 0:
                            if matcher[1]['regex']:
                                c = re.compile(matcher[0]['text'])
                                c = c.findall(dump_response(c))
                                if c:
                                    return alert_bug('INJHEADERS', response, Match=matcher[0]['text'], regex=True, payload=payload, header=h)
                            else:
                                try:
                                    int(matcher[0]['text'])
                                    if payload in response.text:
                                        return alert_bug('INJHEADERS', response, Match=matcher[0]['text'], regex=True, payload=payload, header=h)
                                except:
                                    if matcher[0]['text'] in response.text:
                                        return alert_bug('INJHEADERS', response, Match=matcher['text'], regex=True, payload=payload, header=h)
                    finally :
                        headers[h] = v
