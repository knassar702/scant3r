#!/usr/bin/env python3
__name__ = 'ScanT3r'
__author__ = 'Khaled Nassar'
__email__ = 'knassar702@gmail.com'
__version__ = '0.5#Beta'
from libs import NewRequest as nq
from libs import post_data
from queue import Queue
from threading import Thread
from core import bad
from wordlists import ssrf_parameters

s = Queue()

def GO(url,host):
    for par in ssrf_parameters:
        nq.Get(f"{url.split('?')[0]}/?{par}={host}/{par}")
        nq.Post(url.split('?')[0],post_data(f'{par}={host}/{par}'))
        nq.Put(url.split('?')[0],post_data(f'{par}={host}/{par}'))
def threader(host):
    while True:
        item = s.get()
        GO(item,host)
        s.task_done()
def run(opts):
    global host
    host = opts['host']
    if host == None:
        print(f'{bad} Host Not Found ..!')
    else:
        for i in range(opts['threads']):
            p1 = Thread(target=threader,args=(opts['host'],))
            p1.daemon = True
            p1.start()
        for url in opts['url']:
            s.put(url)
        s.join()