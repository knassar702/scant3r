#!/usr/bin/env python3
from libs import NewRequest as nq
from urllib.parse import urlparse as ur

def parser(url):
    url = url.replace('http://','').replace('https://','')
    return ur(url).path

def httper(url):
    try:
        url = parser(url)
        proto_url = [f'http://{url}',f'https://{url}']
        for url in proto_url:
            r = nq.Get(url)
            if r != 0:
                print(r.url)
    except Exception as e:
        print(e)


def main(opts):
    httper(opts['url'])
