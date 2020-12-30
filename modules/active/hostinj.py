#!/usr/bin/env python3
from libs import NewRequest as nq
from urllib.parse import urlparse
from threading import Thread
from queue import Queue
import sys

q = Queue()

def scan(host):
    try:
        payloads = {
    'scant3r.org':'scant3r.org'
        }
        for payload,msg in payloads.items():
            nq.Update(header={'Host':'scant3r.org'})
            r = nq.Get(host)
            if r != 0:
                try:
                    loc = r.headers.get('Location')
                    if loc:
                        r = urlparse(loc).netloc
                        if 'scant3r.org' in r:
                                print(f'''[+] Found :> {host}''')
                                break
                        else:
                            continue
                finally:
                    pass
    finally:
        pass

def main(opts):
    scan(opts['url'])