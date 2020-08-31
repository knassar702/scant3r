#!/usr/bin/env python3
from libs import NewRequest as nq
from urllib.parse import urljoin
from core import good
from queue import Queue
from threading import Thread

q = Queue()

"""
paths = {
  "/PATH":"MESSAGE",
  "/PATH2":200 # status code
    }
"""
paths = {
    '/phpinfo.php':'PHP Version',
    '/PI.php':'PHP Version',
    '/+CSCOT+/translation-table?type=mst&textdomain=/%2bCSCOE%2b/../../../../..//%2bCSCOE%2b/include/browser_inc.lua&default-language&lang=../':200
        }

def GO(host):
    h = host
    for path,msg in paths.items():
        host = urljoin(host,path)
        try:
            r = nq.Get(host)
            if r != 0:
                try:
                    int(msg)
                    if msg == r.status_code:
                        print(f'{good} Found :> {host}')
                except:
                    if msg in r.content.decode('utf-8'):
                        print(f'{good} Found :> {host}')
        except:
            print('_',end='')
        finally:
            host = h

def threader():
    while True:
        item = q.get()
        GO(item)
        q.task_done()

def run(opts):
    for _ in range(opts['threads']):
        p1 = Thread(target=threader)
        p1.daemon = True
        p1.start()
    for url in opts['url']:
        q.put(url)
    q.join()
