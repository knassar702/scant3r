#!/usr/bin/env python3

from modules import Scan
from core.libs import alert_bug
from wordlists import TLD
from logging import getLogger
import tldextract
from core.libs import Http

log = getLogger('scant3r')

FIREBASE_URL = 'https://%s.firebaseio.com'
class Firebase(Scan):
    def __init__(self, opts: dict, http: Http):
        super().__init__(opts,http)
        
    def start(self) -> dict:
        host = tldextract.extract(self.opts['url']).domain
        log.debug(f"Trying to Find open Firebase database for {host}")
        all_hosts = [host]
        
        for tld in TLD():
            all_hosts.append(host + tld.rstrip())
            
        for target_host in all_hosts:
            firebase = FIREBASE_URL % target_host
            read_request = self.http.send('GET',firebase + '/.json')
            if type(read_request) == list:
                return
            log.debug(f'Check for Read permission -> {host}')
            if read_request.status_code == 200:
                alert_bug('Firebase',read_request,permission="Read enabled",status=200,content_length=len(read_request.text))
            log.debug(f'Check for Write permission -> {host}')
            write_request = self.http.send('PUT',firebase + '/firebase/security.json',body={"msg":"scant3r"},convert_content_type='json',org=False)
            if type(write_request) == list:
                return
            if write_request.status_code == 200:
                alert_bug('Firebase',read_request,permission="Write enabled",status=200,content_length=len(write_request.text))
        
        return {} 
