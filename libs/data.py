#!/usr/bin/env python3
__name__ = 'ScanT3r'
__author__ = 'Khaled Nassar'
__email__ = 'knassar702@gmail.com'
__version__ = '0.5#Beta'

import re
import sys
from core import *
def post_data(params):
    try:
        if params:
            prePostData = params.split("&")
            postData = {}
            for d in prePostData:
                p = d.split("=", 1)
                postData[p[0]] = p[1]
            return postData
        return {}
    except:
        return 0
def extractHeaders(headers):
    headers = headers.replace('\\n', '\n')
    sorted_headers = {}
    matches = re.findall(r'(.*):\s(.*)', headers)
    for match in matches:
        header = match[0]
        value = match[1]
        try:
            if value[-1] == ',':
                value = value[:-1]
            sorted_headers[header] = value
        except IndexError:
            pass
    return sorted_headers

def dump_alloptions(opts):
    for o,v in opts.items():
        x = 1
        if o == 'Headers':
            if v:
                v = True
            else:
                x = 0
        if o == 'list':
            x = 0
        if o == 'module':
            if v:
                pass
            else:
                x = 0
        if o == 'url':
            v = len(v)
            o = 'URLS'
        if o == 'proxy':
            if v:
                v = True
            else:
                x = 0
        if o == 'cookie':
            if v:
                v = True
            else:
                x = 0
        if x == 1:
            module = ""
            if o == 'module':
                for i in v:
                    module += f"{i} "
                print(f'{cyan}[!]{rest} {o} : {module.replace(" ",",")}')
            else:
                print(f'{cyan}[!]{rest} {o} : {v}')
def insertAfter(haystack, needle, newText):
  """ Inserts 'newText' into 'haystack' right after 'needle'. """
  i = haystack.find(needle)
  return haystack[:i + len(needle)] + newText + haystack[i + len(needle):]
