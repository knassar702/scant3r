#!/usr/bin/env python3

from modules import Scan
from core.libs import alert_bug
from wordlists import TLD
from logging import getLogger
from core.libs import Http
import tldextract,concurrent.futures

log = getLogger('scant3r')

FIREBASE_URL = 'https://%s.firebaseio.com'
class Firebase(Scan):
    def __init__(self, opts: dict, http: Http):
        super().__init__(opts,http)
        
    def start(self) -> dict:
        host = tldextract.extract(self.opts['url']).domain
        log.debug(f"Trying to Find open Firebase database for {host}")
        all_hosts = [host]
        tasks = [] 
        for tld in TLD():
            all_hosts.append(host + tld.rstrip())
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            for target_host in all_hosts:
                tasks.append(executor.submit(self.scan,target_host)) 
    def scan(self,target_host):
        firebase = FIREBASE_URL % target_host
        read_request = self.http.send('GET',firebase + '/.json')
        if type(read_request) == list:
            return
        log.debug(f'Check for Read permission -> {firebase}')
        if read_request.status_code == 200:
            alert_bug('Firebase',read_request,permission="Read enabled",status=200,content_length=len(read_request.text))
        log.debug(f'Check for Write permission -> {firebase}')
        write_request = self.http.send('PUT',firebase + '/firebase/security.json',body={"msg":"scant3r"},org=False)
        if type(write_request) == list:
            return
        if write_request.status_code == 200:
            alert_bug('Firebase',read_request,permission="Write enabled",status=200,content_length=len(write_request.text))
        
        return {} 
