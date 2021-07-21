#!/usr/bin/env python3

from modules import Scan
from core.libs import alert_bug
from urllib.parse import urlparse
from wordlists import TLD
import tldextract

class Firebase(Scan):
    def __init__(self,opts,http):
        super().__init__(opts,http)
    def start(self):
        host = tldextract.extract(self.opts['url']).domain
        all_hosts = [host]
        for tld in TLD():
            all_hosts.append(host + tld.rstrip())
        for target_host in all_hosts:
            firebase = 'https://%s.firebaseio.com' % target_host
            read_request = self.http.send('GET',firebase + '/.json')
            write_request = self.http.send('PUT',firebase + '/firebase/security.json',body={"msg":"scant3r"},contentType='json',org=False)
            if read_request.status_code == 200:
                alert_bug('Firebase',read_request,permission="Read enabled",status=200,content_length=len(read_request.text))
            if write_request.status_code == 200:
                alert_bug('Firebase',read_request,permission="Write enabled",status=200,content_length=len(write_request.text))
        return {} 
