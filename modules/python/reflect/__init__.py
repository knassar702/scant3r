from .reflect import Scan
from urllib.parse import urlparse
from core.libs import show_error

def main(opts,r):
    if urlparse(opts['url']).query:
        v = Scan(opts, r).scan()
        if v:
            for i in v.keys():
                print(f'[Refelct] Found :> {v[i]} {i}')
    else: 
        show_error('reflect', "No query in the URL")