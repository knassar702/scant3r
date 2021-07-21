from .reflect import Reflect
from urllib.parse import urlparse
from core.libs import show_error, Http

def main(opts: dict, http: Http):
    if urlparse(opts['url']).query:
        list_result = Reflect(opts, http).start()
        if list_result:
            for i in list_result.keys():
                print(f'[Refelct] Found :> {list_result[i]} {i}')
    else: 
        show_error('reflect', "No query in the URL")