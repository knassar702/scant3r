#!/usr/bin/env python3
from urllib.parse import urljoin
from core.libs import Colors as c
from yaml import safe_load
from core.libs import alert_bug, Http
from modules import Scan
from logging import getLogger

log = getLogger('scant3r')

class Paths(Scan):
    def __init__(self, opts: dict, http: Http):
        super().__init__(opts, http)
    
    def start(self) -> list:
        found = []
        log.debug('load paths config file')
        f = safe_load(open('modules/python/paths/conf.yaml','r')) 
        for path, msg in f.items(): 
            log.debug('insert the path to url')
            if path.startswith('/'):
                path = path[1:]
            host = urljoin(self.opts['url'], path)
            try:
                log.debug('send http request to the target')
                response = self.http.send('GET',host)
                if response != 0:
                    try:
                        msg = int(msg)
                        log.debug('matching by http status code')
                        if msg == response.status_code:
                            alert_bug('paths', response, found=host, match=f'status Code: [{response.status_code}]')
                    except:
                        log.debug('matching by http response body')
                        if msg in response.text:
                            alert_bug('paths', response, found=host, match=f'Text: {msg}')
            except Exception as e:
                log.error(e)
            finally: 
                host = self.opts['url']
        return found 
