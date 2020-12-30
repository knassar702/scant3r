#!/usr/bin/env python3

from requests import get
from core import good,cyan,rest,bmagenta,Byellow,yellow,magenta

def RNG(host):
    try:
        r = get(host,headers={'Range':'bytes=0-,1-1,2-2,3-3,4-4,5-5,6-6'},verify=False,allow_redirects=False)
        if 'Content-Range: bytes'.encode('utf-8') in r.content:
            print(f'''
{yellow}[ {cyan}RANGE HEADER{rest} {yellow}]
{good} Found >> {host}
{"-"*13}|
''')
    except:
        pass
def main(opts):
    RNG(opts['url'])
