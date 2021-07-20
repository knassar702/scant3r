#!/usr/bin/env python3
from urllib.parse import urljoin
from core.libs import Colors as c
from yaml import safe_load
from core.libs import alert_bug
from modules import Scan
from logging import getLogger

log = getLogger('scant3r')

class Paths(Scan):
    def __init__(self, opts, http):
        super().__init__(opts, http)
    
    def start(self) -> list:
        found = []
        log.debug('load paths config file')
        f = safe_load(open('modules/python/paths/conf.yaml','r')) 
        for path, msg in f.items(): 
            log.debug('insert path to url')
            host = urljoin(self.opts['url'], path)
            try:
                log.debug('send http request to the target')
                r = self.http.send('GET',host)
                if r != 0:
                    try:
                        if msg == r.status_code:
                            alert_bug('paths',r,found=host,match=f'status Code: [{r.status_code}]')
                    except:
                        if msg in r.text:
                            alert_bug('paths',r,found=host,match=f'Text: {r.text}')
            except Exception as e:
                log.error(e)
            finally: 
                host = self.opts['url']
        return found 
