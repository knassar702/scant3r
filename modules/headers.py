#!/usr/bin/env python3
__name__ = 'ScanT3r'
__author__ = 'Khaled Nassar'
__email__ = 'knassar702@gmail.com'
__version__ = '0.5#Beta'

from requests import get,post,put
from libs import NewRequest as nq
from libs import post_data,insertAfter,extractHeaders
from core import ShowMessage as show
from urllib.parse import urlparse
from random import randint
from threading import Thread
from requests_toolbelt.utils import dump
from queue import Queue
from re import search,findall
from wordlists import *

SCAN_Headers = [
    'User-agent',
    'referer'
    ] # add you headers here UwU




xss_payloads = XP.Dump()


def new_req(method='GET',Dump=None,proxy=None,url=None,redirect=False,data=None,timeout=10,headers={},cookies=None):
    method = method.upper()
    if data:
        data = post_data(data)
    if method == 'GET':
        r = get(url=url,proxies=proxy,cookies=cookies,allow_redirects=redirect,timeout=timeout,verify=False,headers=headers)
    if method == 'POST':
        r = post(url=url,data=data,proxies=proxy,allow_redirects=redirect,verify=False,timeout=timeout,cookies=cookies,headers=headers)
    if method == 'PUT':
        r = put(url=url,data=data,proxies=proxy,allow_redirects=redirect,verify=False,cookies=cookies,timeout=timeout,headers=headers)
    if Dump:
        d_r = dump.dump_all(r)
        print(d_r.decode())
    return r

def xss_header_thread(q):
    while True:
        item = q.get()
        H_Xss.Get(item)
        H_Xss.Post(item)
        H_Xss.Put(item)
        q.task_done()
def sqli_header_thread(q):
    while True:
        item = q.get()
        H_Sqli.Get(item)
        H_Sqli.Post(item)
        H_Sqli.Put(item)
        q.task_done()
def ssti_header_thread(q):
    while True:
        item = q.get()
        H_SSTI.Get(item)
        H_SSTI.Post(item)
        H_SSTI.Put(item)
        q.task_done()
def rce_header_thread(q):
    while True:
        item = q.get()
        H_RCE.Get(item)
        H_RCE.Post(item)
        H_RCE.Put(item)
        q.task_done()

class save_request:
    def save(request):
        global r
        r = request
        return r
    def get():
        return r
def REQ(url=None,data=None,method='GET',headers=None):
    d = nq.Dump()
    return new_req(url=url,proxy=d['proxy'],Dump=d['dump'],method=method,headers=headers,timeout=d['timeout'],redirect=d['redirect'],cookies=d['cookies'],data=data)
def Back_H(opt):
    return nq.Update(redirect=opt['redirect'],dump=opt['dump'],cookie=opt['cookies'],header=opt['headers'],timeout=opt['timeout'],proxies=opt['proxy'],random_agents=opt['random_agents'])
class H_Xss:
    def Get(url):
        all_headers = {}
        d = nq.Dump()
        for header in SCAN_Headers:
            for payload in xss_payloads:
                try:
                    H = nq.Dump()['headers'][header]
                    P =f'{H}{payload}'
                except:
                    P = payload
                for H,V in d['headers'].items():
                    if H == header:
                        pass
                    else:
                        all_headers[H] = V
                all_headers[header] = P
                req = REQ(url,headers=all_headers)
                if req != 0:
                    if payload.encode('utf-8') in req.content:
                        show.bug_Header(bug='Cross-site scripting',payload=payload,method='GET',header=header,target=url)
                        break
    def Post(url):
        d = nq.Dump()
        for header in SCAN_Headers:
            for payload in xss_payloads:
                all_headers = {}
                try:
                    url.split('?')[1].split('&')
                    data = urlparse(url).query
                    data = post_data(data)
                    if data == 0:
                        data = {}
                except:
                    data = {}
                try:
                    H = nq.Dump()['headers'][header]
                    P =f'{H}{payload}'
                except:
                    P = payload
                for H,V in d['headers'].items():
                    if H == header:
                        pass
                    else:
                        all_headers[H] = V
                all_headers[header] = P
                req = REQ(url.split('?')[0],data=data,headers=all_headers,method='POST')
                if req == 0:
                    break
                if payload.encode('utf-8') in req.content:
                    show.bug_Header(bug='Cross-site scripting',payload=payload,method='POST',header=header,target=url)
                    break
    def Put(url):
        d = nq.Dump()
        for header in SCAN_Headers:
            for payload in xss_payloads:
                all_headers = {}
                try:
                    url.split('?')[1].split('&')
                    data = urlparse(url).query
                    data = post_data(data)
                    if data == 0:
                        data = {}
                except:
                    data = {}
                try:
                    H = nq.Dump()['headers'][header]
                    P =f'{H}{payload}'
                except:
                    P = payload
                for H,V in d['headers'].items():
                    if H == header:
                        pass
                    else:
                        all_headers[H] = V
                all_headers[header] = P
                req = REQ(url.split('?')[0],data=data,method='PUT',headers=all_headers)
                if req == 0:
                    break
                if payload.encode('utf-8') in req.content:
                    show.bug_Header(bug='Cross-site scripting',payload=payload,method='PUT',header=header,target=url)
                    break


class H_Sqli:
    def Get(url):
        d = nq.Dump()
        for header in SCAN_Headers:
            for payload in sqli_payloads:
                all_headers = {}
                r = nq.Get(url)
                if r == 0:
                    break
                save_request.save(r)
                try:
                    H = nq.Dump()['headers'][header]
                    P =f'{H}{payload}'
                except:
                    P = payload
                for H,V in d['headers'].items():
                    if H == header:
                        pass
                    else:
                        all_headers[H] = V
                all_headers[header] = P
                req = REQ(url.split('?')[0],method='GET',headers=all_headers)
                if req == 0:
                    break
                for n,e in sql_err.items():
                    r2 = findall(e.encode('utf-8'),save_request.get().content)
                    r3 = findall(e.encode('utf-8'),req.content)
                    if len(r2) < len(r3):
                        show.bug_Header(bug='SQL injection',payload=payload,method='GET',header=header,target=url)
                        break
    def Post(url):
        d = nq.Dump()
        for header in SCAN_Headers:
            for payload in sqli_payloads:
                all_headers = {}
                try:
                    url.split('?')[1].split('&')
                    data = urlparse(url).query
                    data = post_data(data)
                    if data == 0:
                        data = {}
                except:
                    data = {}
                r = nq.Post(url,data)
                if r == 0:
                    break
                save_request.save(r)
                try:
                    H = nq.Dump()['headers'][header]
                    P =f'{H}{payload}'
                except:
                    P = payload
                for H,V in d['headers'].items():
                    if H == header:
                        pass
                    else:
                        all_headers[H] = V
                all_headers[header] = P
                req = REQ(url.split('?')[0],data=data,method='POST',headers=all_headers)
                if req == 0:
                    break
                for n,e in sql_err.items():
                    r = findall(e.encode('utf-8'),save_request.get().content)
                    r2 = findall(e.encode('utf-8'),req.content)
                    if len(r) < len(r2):
                        show.bug_Header(bug='SQL injection',payload=payload,method='POST',header=header,target=url)
                        break
    def Put(url):
        d = nq.Dump()
        for header in SCAN_Headers:
            for payload in sqli_payloads:
                all_headers = {}
                try:
                    url.split('?')[1].split('&')
                    data = urlparse(url).query
                    data = post_data(data)
                    if data == 0:
                        data = {}
                except:
                    data = {}
                r = nq.Put(url,data)
                if r == 0:
                    break
                save_request.save(r)
                try:
                    H = nq.Dump()['headers'][header]
                    P =f'{H}{payload}'
                except:
                    P = payload
                for H,V in d['headers'].items():
                    if H == header:
                        pass
                    else:
                        all_headers[H] = V
                all_headers[header] = P
                req = REQ(url.split('?')[0],data=data,method='PUT',headers=all_headers)
                if req == 0:
                    break
                for n,e in sql_err.items():
                    r = findall(e.encode('utf-8'),save_request.get().content)
                    r2 = findall(e.encode('utf-8'),req.content)
                    if len(r) < len(r2):
                        show.bug_Header(bug='SQL injection',payload=payload,method='PUT',header=header,target=url)
                        break
class H_RCE:
    def Get(url):
        d = nq.Dump()
        for header in SCAN_Headers:
            for payload,message in rce_payloads.items():
                all_headers = {}
                payload = payload.replace('\n','%0a')
                r = nq.Get(url)
                if r == 0:
                    break
                r = len(findall(message.encode('utf-8'),r.content))
                try:
                    H = nq.Dump()['headers'][header]
                    P =f'{H}{payload}'
                except:
                    P = payload
                for H,V in d['headers'].items():
                    if H == header:
                        pass
                    else:
                        all_headers[H] = V
                all_headers[header] = P
                req = REQ(url.split('?')[0],method='GET',headers=all_headers)
                if req == 0:
                    break
                if r < len(findall(message.encode('utf-8'),req.content)):
                    show.bug_Header(bug='command injection',payload=payload.replace('\n','%0a'),method='GET',header=header,target=url)
                    break
    def Post(url):
        d = nq.Dump()
        for header in SCAN_Headers:
            for payload,message in rce_payloads.items():
                all_headers = {}
                payload = payload.replace('\n','%0a')
                try:
                    url.split('?')[1].split('&')
                    data = urlparse(url).query
                    data = post_data(data)
                    if data == 0:
                        data = {}
                except:
                    data = {}
                r = nq.Post(url.split('?')[0],data)
                if r == 0:
                    break
                r = len(findall(message.encode('utf-8'),r.content))
                try:
                    H = nq.Dump()['headers'][header]
                    P =f'{H}{payload}'
                except:
                    P = payload
                for H,V in d['headers'].items():
                    if H == header:
                        pass
                    else:
                        all_headers[H] = V
                all_headers[header] = P
                req = REQ(url.split('?')[0],data=data,method='POST',headers=all_headers)
                if req == 0:
                    break
                if r < len(findall(message.encode('utf-8'),req.content)):
                    show.bug_Header(bug='command injection',payload=payload.replace('\n','%0a'),method='POST',header=header,target=url)
                    break
    def Put(url):
        d = nq.Dump()
        for header in SCAN_Headers:
            for payload,message in rce_payloads.items():
                all_headers = {}
                payload = payload.replace('\n','%0a')
                try:
                    url.split('?')[1].split('&')
                    data = urlparse(url).query
                    data = post_data(data)
                    if data == 0:
                        data = {}
                except:
                    data = {}
                r = nq.Put(url.split('?')[0],data)
                if r == 0:
                    break
                r = len(findall(message.encode('utf-8'),r.content))
                try:
                    H = nq.Dump()['headers'][header]
                    P =f'{H}{payload}'
                except:
                    P = payload
                for H,V in d['headers'].items():
                    if H == header:
                        pass
                    else:
                        all_headers[H] = V
                all_headers[header] = P
                req = REQ(url.split('?')[0],data=data,method='PUT',headers=all_headers)
                if req == 0:
                    break
                if r < len(findall(message.encode('utf-8'),req.content)):
                    show.bug_Header(bug='command injection',payload=payload.replace('\n','%0a'),method='PUT',header=header,target=url)
                    break
class H_SSTI:
    def Get(url):
        d = nq.Dump()
        for header in SCAN_Headers:
            for payload,message in ssti_payloads.items():
                all_headers = {}
                r = nq.Get(url)
                if r == 0:
                    break
                r = len(findall(message.encode('utf-8'),r.content))
                try:
                    H = nq.Dump()['headers'][header]
                    P =f'{H}{payload}'
                except:
                    P = payload
                for H,V in d['headers'].items():
                    if H == header:
                        pass
                    else:
                        all_headers[H] = V
                all_headers[header] = P
                req = REQ(url.split('?')[0],headers=all_headers)
                if req == 0:
                    break
                if r < len(findall(message.encode('utf-8'),req.content)):
                    show.bug_Header(bug='template injection',payload=payload,method='GET',header=header,target=url)
                    break
    def Post(url):
        d = nq.Dump()
        for header in SCAN_Headers:
            for payload,message in ssti_payloads.items():
                all_headers = {}
                try:
                    url.split('?')[1].split('&')
                    data = urlparse(url).query
                    data = post_data(data)
                    if data == 0:
                        data = {}
                except:
                    data = {}
                r = nq.Post(url.split('?')[0],data)
                if r == 0:
                    break
                r = len(findall(message.encode('utf-8'),r.content))
                try:
                    H = nq.Dump()['headers'][header]
                    P =f'{H}{payload}'
                except:
                    P = payload
                for H,V in d['headers'].items():
                    if H == header:
                        pass
                    else:
                        all_headers[H] = V
                all_headers[header] = P
                req = REQ(url.split('?')[0],headers=all_headers,data=data,method='POST')
                if req == 0:
                    break
                if r < len(findall(message.encode('utf-8'),req.content)):
                    show.bug_Header(bug='template injection',payload=payload,method='POST',header=header,target=url)
                    break
    def Put(url):
        d = nq.Dump()
        for header in SCAN_Headers:
            for payload,message in ssti_payloads.items():
                all_headers = {}
                try:
                    url.split('?')[1].split('&')
                    data = urlparse(url).query
                    data = post_data(data)
                    if data == 0:
                        data = {}
                except:
                    data = {}
                r = nq.Put(url.split('?')[0],data)
                if r == 0:
                    break
                r = len(findall(message.encode('utf-8'),r.content))
                try:
                    H = nq.Dump()['headers'][header]
                    P =f'{H}{payload}'
                except:
                    P = payload
                for H,V in d['headers'].items():
                    if H == header:
                        pass
                    else:
                        all_headers[H] = V
                req = REQ(url.split('?')[0],headers=all_headers,data=data,method='PUT')
                if req == 0:
                    break
                if r < len(findall(message.encode('utf-8'),req.content)):
                    show.bug_Header(bug='template injection',payload=payload,method='PUT',header=header,target=url)
                    break

f = Queue()
t = Queue()
y = Queue()
u = Queue()

def run(opts):
    for i in range(opts['threads']):
        p1 = Thread(target=xss_header_thread,args=(f,))
        p1.daemon = True
        p1.start()
        p2 = Thread(target=sqli_header_thread,args=(t,))
        p2.daemon = True
        p2.start()
        p3 = Thread(target=rce_header_thread,args=(y,))
        p3.daemon = True
        p3.start()
        p4 = Thread(target=ssti_header_thread,args=(u,))
        p4.daemon = True
        p4.start()
    for url in opts['url']:
        f.put(url)
        t.put(url)
        y.put(url)
        u.put(url)
    f.join()
    u.join()
    y.join()
    t.join()
