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
def threader():
    while True:
        item = q.get()
        scan(item)
        q.task_done()

def run(opts):
    for _ in range(opts['threads']):
        p1 = Thread(target=threader)
        p1.daemon = True
        p1.start()
    for url in opts['url']:
        q.put(url)
    q.join()
    sys.exit()
