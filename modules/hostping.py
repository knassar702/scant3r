#!/usr/bin/env python3
from socket import gethostbyname as ping
from queue import Queue
from threading import Thread

q = Queue()

def start(host):
    try:
        host = host.replace('http://','').replace('https://','')
        HOST = ping(host)
        print(f'{host} {HOST}')
    except:
        pass
def threader():
    while True:
        item = q.get()
        start(item)
        q.task_done()

def run(opts):
    for _ in range(opts['threads']):
        p = Thread(target=threader)
        p.daemon = True
        p.start()
    for host in opts['url']:
        q.put(host)
    q.join()
