#!/usr/bin/env python3
from libs import NewRequest as nq
from urllib.parse import urljoin
from threading import Thread
from queue import Queue


q = Queue()

def scan(host):
    try:
        payloads = {
    'scan{{6*6}}t3r':'scan36t3r',
    'scan${6*6}t3r':'scan36t3r',
    'scan<% 6*6 %>t3r':'scan36t3r'
        }
        for payload,msg in payloads.items():
            new_host = urljoin(host,f'{payload}')
            r = nq.Get(new_host)
            if r != 0:
                if msg.encode('utf-8') in r.content:
                    print(f'''
[+] Found :> {new_host}
                ''')
                    break
                else:
                    continue
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
