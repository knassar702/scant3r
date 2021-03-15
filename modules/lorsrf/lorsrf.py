#!/usr/bin/env python3
__name__ = 'ScanT3r'
__author__ = 'Khaled Nassar'
__email__ = 'knassar702@gmail.com'
__version__ = '0.6#Beta'
from core.libs import post_data,urlencoder,bad
from urllib.parse import urlparse # url parsing
from wordlists import ssrf_parameters # ssrf parameters wordlist


parameters_in_one_request = 10
# parameters_in_one_request = 2
# ?ex1=http://google.com&ex2=http://google.com

def start(url,host,http,methods=['GET','POST']):
    l = len(ssrf_parameters())
    newurl = url
    for method in methods:
        for par in ssrf_parameters():
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
                if method == 'GET':
                    http.send('GET',newurl)
                else:
                    http.send(method,url.split('?')[0],body=urlparse(newurl).query)
                newurl = url


