#!/usr/bin/env python3
__name__ = 'ScanT3r'
__author__ = 'Khaled Nassar'
__email__ = 'knassar702@gmail.com'
__version__ = '0.6#Beta'

from libs import NewRequest as nq
from libs import post_data,insertAfter
from libs import urlencoder as en
from core import ShowMessage as show
from urllib.parse import urlparse
from random import randint
from re import search,findall
from wordlists import *
class save_request:
    def save(request):
        global r
        r = request
        return r
    def get():
        return r
xss_payloads = XP.Dump()

class Xss:
    def Get(url):
        for param in url.split("?")[1].split("&"):
            for payload in xss_payloads:
                req = nq.Get(url.replace(param,param + en(payload)))
                if req != 0:
                    if payload.encode('utf-8') in req.content:
                        bug = {
                                'name':'Corss-site scripting',
                                'payload':payload,
                                'method':'GET',
                                'parameter':param,
                                'link':url.replace(param,param + en(payload))
                                }
                        show.bug(bug='Cross-site scripting',payload=payload,method='GET',parameter=param,link=url.replace(param,param + en(payload)))
                        return bug
        return None
    def Post(url):
        for param in url.split('?')[1].split('&'):
            for payload in xss_payloads:
                data = urlparse(url.replace(param,param + payload)).query
                d = post_data(data)
                if d == 0:
                    break
                req = nq.Post(url.split('?')[0],post_data(data))
                if req == 0:
                    break
                if payload.encode('utf-8') in req.content:
                    bug = {
                            'name':'Corss-site scripting',
                            'payload':payload,
                            'method':'POST',
                            'parameter':param,
                            'target':url.split('?')[0],
                            'data':data
                            }
                    show.bug(bug='Cross-site scripting',payload=payload,method='POST',parameter=param,target=url.split('?')[0],link=data)
                    return bug
        return None
    def Put(url):
        for param in url.split('?')[1].split('&'):
            for payload in xss_payloads:
                data = urlparse(url.replace(param,param + payload)).query
                d = post_data(data)
                if d == 0:
                    break
                req = nq.Put(url.split('?')[0],post_data(data))
                if req == 0:
                    break
                if payload.encode('utf-8') in req.content:
                    bug = {
                            'name':'Corss-site scripting',
                            'payload':payload,
                            'method':'PUT',
                            'parameter':param,
                            'target':url.split('?')[0],
                            'data':data
                            }
                    show.bug(bug='Cross-site scripting',payload=payload,method='PUT',parameter=param,target=url.split('?')[0],link=data)
                    return bug
        return None

class Sqli:
    def Get(url):
        for param in url.split('?')[1].split('&'):
            for payload in sqli_payloads:
                r = nq.Get(url)
                if r == 0:
                    break
                save_request.save(r)
                req = nq.Get(url.replace(param,param + payload))
                if req == 0:
                    break
                for n,e in sql_err.items():
                    r2 = findall(e.encode('utf-8'),save_request.get().content)
                    r3 = findall(e.encode('utf-8'),req.content)
                    if len(r2) < len(r3):
                        bug = {
                                'name':'SQL injection',
                                'payload':payload,
                                'method':'GET',
                                'parameter':param,
                                'link':url.replace(param,param + en(payload)),
                                'target':url.split('?')[0]
                                }
                        show.bug(bug='SQL injection',payload=payload,method='GET',parameter=param,target=url.split('?')[0],link=url.replace(param,param + en(payload)))
                        return bug
        return None
    def Post(url):
        for param in url.split('?')[1].split('&'):
            for payload in sqli_payloads:
                d = post_data(urlparse(url).query)
                if d == 0:
                    break
                r = nq.Post(url,post_data(urlparse(url).query))
                if r == 0:
                    break
                save_request.save(r)
                data = urlparse(url.replace(param,param + payload)).query
                req = nq.Post(url.split('?')[0],post_data(data))
                if req == 0:
                    break
                for n,e in sql_err.items():
                    r = findall(e.encode('utf-8'),save_request.get().content)
                    r2 = findall(e.encode('utf-8'),req.content)
                    if len(r) < len(r2):
                        bug = {
                            'name':'SQL injection',
                            'payload':payload,
                            'method':'POST',
                            'parameter':param,
                            'target':url.split('?')[0],
                            'data':data
                            }
                        show.bug(bug='SQL injection',payload=payload,method='POST',parameter=param,target=url.split('?')[0],link=data)
                        return bug
        return None
    def Put(url):
        for param in url.split('?')[1].split('&'):
            for payload in sqli_payloads:
                if post_data(urlparse(url).query) == 0:
                    break
                r = nq.Put(url,post_data(urlparse(url).query))
                if r == 0:
                    break
                save_request.save(r)
                data = urlparse(url.replace(param,param+payload)).query
                req = nq.Put(url.split('?')[0],post_data(data))
                if req == 0:
                    break
                for n,e in sql_err.items():
                    r = findall(e.encode('utf-8'),save_request.get().content)
                    r2 = findall(e.encode('utf-8'),req.content)
                    if len(r) < len(r2):
                        bug = {
                            'name':'SQL injection',
                            'payload':payload,
                            'method':'PUT',
                            'parameter':param,
                            'target':url.split('?')[0],
                            'data':data
                            }
                        show.bug(bug='SQL injection',payload=payload,method='PUT',parameter=param,target=url.split('?')[0],link=data)
                        return bug
        return None
class RCE:
    def Get(url):
        for param in url.split('?')[1].split('&'):
            for payload,message in rce_payloads.items():
                r = nq.Get(url)
                if r == 0:
                    break
                r = len(findall(message.encode('utf-8'),r.content))
                req = nq.Get(url.replace(param,param + en(payload)))
                if req == 0:
                    break
                if r < len(findall(message.encode('utf-8'),req.content)):
                    bug = {
                            'name':'command injection',
                            'payload':payload.replace('\n','%0a'),
                            'method':'GET',
                            'parameter':param,
                            'link':url.replace(param,param + en(payload)),
                            'target':url.split('?')[0]
                        }
                    show.bug(bug='command injection',payload=payload.replace('\n','%0a'),method='GET',parameter=param,link=url.replace(param,param + en(payload)))
                    return bug
        return None
    def Post(url):
        for param in url.split('?')[1].split('&'):
            for payload,message in rce_payloads.items():
                if post_data(urlparse(url).query) == 0:
                    break
                r = nq.Post(url.split('?')[0],post_data(urlparse(url).query))
                if r == 0:
                    break
                r = len(findall(message.encode('utf-8'),r.content))
                data = urlparse(url.replace(param,param + payload)).query
                req = nq.Post(url.split('?')[0],post_data(data))
                if req == 0:
                    break
                if r < len(findall(message.encode('utf-8'),req.content)):
                    bug = {
                        'name':'command injection',
                        'payload':payload.replace('\n','%0a'),
                        'method':'POST',
                        'parameter':param,
                        'target':url.split('?')[0],
                        'data':data
                        }
                    show.bug(bug='command injection',payload=payload.replace('\n','%0a'),method='POST',parameter=param,target=url.split('?')[0],link=data.replace('\n','%0a'))
                    return bug
        return None
    def Put(url):
        for param in url.split('?')[1].split('&'):
            for payload,message in rce_payloads.items():
                if post_data(urlparse(url).query) == 0:
                    break
                r = nq.Put(url.split('?')[0],post_data(urlparse(url).query))
                if r == 0:
                    break
                r = len(findall(message.encode('utf-8'),r.content))
                data = urlparse(url.replace(param,param + payload)).query
                req = nq.Put(url.split('?')[0],post_data(data))
                if req == 0:
                    break
                if r < len(findall(message.encode('utf-8'),req.content)):
                    bug = {
                        'name':'command injection',
                        'payload':payload.replace('\n','%0a'),
                        'method':'POST',
                        'parameter':param,
                        'target':url.split('?')[0],
                        'data':data
                        }
                    show.bug(bug='command injection',payload=payload.replace('\n','%0a'),method='PUT',parameter=param,target=url.split('?')[0],link=data.replace('\n','%0a'))
                    return bug
        return None
class SSTI:
    def Get(url):
        for param in url.split('?')[1].split('&'):
            for payload,message in ssti_payloads.items():
                r = nq.Get(url)
                if r == 0:
                    break
                r = len(findall(message.encode('utf-8'),r.content))
                req = nq.Get(url.replace(param,param + en(payload)))
                if req == 0:
                    break
                if r < len(findall(message.encode('utf-8'),req.content)):
                    bug = {
                            'name':'template injection',
                            'payload':payload,
                            'method':'GET',
                            'parameter':param,
                            'link':url.replace(param,param + en(payload)),
                            'target':url.split('?')[0]
                        }
                    show.bug(bug='template injection',payload=payload,method='GET',parameter=param,link=url.replace(param,param + en(payload)))
                    return bug
        return None
    def Post(url):
        for param in url.split('?')[1].split('&'):
            for payload,message in ssti_payloads.items():
                if post_data(urlparse(url).query) == 0:
                    break
                r = nq.Post(url.split('?')[0],post_data(urlparse(url).query))
                if r == 0:
                    break
                r = len(findall(message.encode('utf-8'),r.content))
                data = urlparse(url.replace(param,param + payload)).query
                req = nq.Post(url.split('?')[0],post_data(data))
                if req == 0:
                    break
                if r < len(findall(message.encode('utf-8'),req.content)):
                    bug = {
                        'name':'template injection',
                        'payload':payload,
                        'method':'POST',
                        'parameter':param,
                        'target':url.split('?')[0],
                        'data':data
                        }
                    show.bug(bug='template injection',payload=payload,method='POST',parameter=param,target=url.split('?')[0],link=data)
                    return bug
        return None
    def Put(url):
        for param in url.split('?')[1].split('&'):
            for payload,message in ssti_payloads.items():
                if post_data(urlparse(url).query) == 0:
                    break
                r = nq.Put(url.split('?')[0],post_data(urlparse(url).query))
                if r == 0:
                    break
                r = len(findall(message.encode('utf-8'),r.content))
                data = urlparse(url.replace(param,param + payload)).query
                req = nq.Put(url.split('?')[0],post_data(data))
                if req == 0:
                    break
                if r < len(findall(message.encode('utf-8'),req.content)):
                    bug = {
                        'name':'template injection',
                        'payload':payload,
                        'method':'PUT',
                        'parameter':param,
                        'target':url.split('?')[0],
                        'data':data
                        }
                    show.bug(bug='template injection',payload=payload,method='PUT',parameter=param,target=url.split('?')[0],link=data)
                    return bug
        return None
class CRLF:
    def Get(url):
        for param in url.split('?')[1].split('&'):
            for payload in crlf_payloads:
                r = nq.Get(url.replace(param,param + en(payload)))
                if r == 0:
                    break
                if r.headers.get('Header-Test'):
                    bug = {
                            'name':'CRLF injection',
                            'payload':payload.replace('\n','%0a').replace('\r','%0d'),
                            'method':'GET',
                            'parameter':param,
                            'link':url.replace(param,param + en(payload)),
                            'target':url.split('?')[0]
                        }
                    show.bug(
                    bug='CRLF injection',
                    payload=payload.replace('\n','%0a').replace('\r','%0d'),
                    method='GET',
                    parameter=param,
                    link=url.replace(param,param + en(payload))
                            )
                    return bug
                else:
                    continue
        return None