#!/usr/bin/env python3
__name__ = 'ScanT3r'
__author__ = 'Khaled Nassar'
__email__ = 'knassar702@gmail.com'
__version__ = '0.6#Beta'
from libs import NewRequest as nq
from libs import post_data,urlencoder 
from core import bad # color
from urllib.parse import urlparse # url parsing
from wordlists import ssrf_parameters # ssrf parameters wordlist
import sys


parameters_in_one_request = 10
# parameters_in_one_request = 2
# ?ex1=http://google.com&ex2=http://google.com

def GO(url,host):
    l = len(ssrf_parameters)
    newurl = url
    for par in ssrf_parameters:
        pay = f'{host}/{par}'
        if newurl != url:
            if len(urlparse(newurl).query) > 0:
                newurl += f'&{par}={pay}'
            else:
                newurl += f'?{par}={pay}'
        else:
            if len(urlparse(url).query) > 0:
                newurl += f'&{par}={pay}'
            else:
                newurl += f'?{par}={pay}'
        if len(urlparse(newurl).query.split('=')) == parameters_in_one_request + 1:
            nq.Get(newurl)
            nq.Post(url.split('?')[0],post_data(urlparse(newurl).query))
            newurl = url

def main(opts):
    host = opts['host']
    if host == None:
        print(f'{bad} Host Not Found ..!') # -x option (ex: -x http://knassar702.burpcal.com)
        sys.exit()
    else:
        GO(opts['url'],host)
