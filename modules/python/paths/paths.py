#!/usr/bin/env python3
from urllib.parse import urljoin
from core.libs import Colors as c
from yaml import safe_load
from scan import Scan
class Paths(Scan):
    def __init__(self, opts, http):
        super().__init__(opts, http)
    
    def start(self) -> list:
        found = []
        f = safe_load(open('modules/python/paths/conf.yaml','r')) 
        for path, msg in f.items(): 
            host = urljoin(self.opts['url'], path)
            try: 
                r = self.http.send('GET',host)
                if r != 0:
                    try:
                        if msg == r.status_code: 
                            print(f'{c.good} Found :> {host}')
                            found.append(host)
                    except :
                        if msg in r.text:
                            print(f'{c.good} Found :> {host}')
                            found.append(host)
            except:
                pass 
            finally: 
                host = self.opts['url']
        return found 