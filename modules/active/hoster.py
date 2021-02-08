#!/usr/bin/env python3
from requests import get
from urllib.parse import urlparse
from core import bad,good
import sys


def newreq(host,header=None):
    try:
        if header:
            r = get(host,headers={'Host':header},verify=False,allow_redirects=False)
        else:
            r = get(host,verify=False,allow_redirects=False)
        return r
    except Exception as e:
        print(f'{bad} {e}')
        return 0
# 0 = Location header value
# 1 = status code && content-length

payloads = [
    'scant3r.org',
    'localhost',
    'dev',
    'test',
    'testing',
    '127.0.0.1',
    '0.0.0.0'
    ]

def scan(host):
    try:
        for payload in payloads:
            r = newreq(host,payload)
            r2 = newreq(host)
            if r != 0 and r2 != 0:
                try:
                    if 1==1:
                        loc = r.headers.get('Location')
                        if loc:
                            R = urlparse(loc).netloc
                            if 'scant3r.org' in R:
                                    print(f'{good} Found :> {host} | {R}')
                            else:
                                if r.status_code != r2.status_code and r.status_code not in (404,500):
                                    print(f'{good} Found :> {host} | {payload} (WITH:{r.status_code}| WITHOUT:{r2.status_code})')
                                    if len(r.content) != len(r2.content):
                                        print(f'{good} Found :> {host} | {payload} (WITH:{len(r.content)}| WITHOUT:{len(r2.content)})')
                except Exception as e:
                    print(f'{bad} {e}')
    except Exception as e:
        print(f'{bad} {e}')

def main(opts):
    scan(opts['url'])