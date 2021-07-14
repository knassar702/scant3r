#!/usr/bin/env python3
__author__ = 'Khaled Nassar'
__email__ = 'knassar702@gmail.com'
__version__ = '0.7#Beta'

import re
import binascii
import random
import string
from urllib.parse import urljoin, urlparse
from .colors import *


def random_str(num):
    num = int(num)
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(num))

def dump_request(request):
    if request == 0:
        return ''
    body = ""
    body += request.request.method
    body += " "
    body += request.request.url + ' HTTP/1.1'
    body += "\n"

    for header,value in request.request.headers.items():
        body += header + ": " + value + "\n"

    if request.request.body != None:
        body += '\n' + str(request.request.body)
    return body

def dump_response(request):
    if request == 0:
        return ''
    body = "HTTP /1.1 "
    body += str(request.status_code)
    body += " "
    body += request.reason
    body += "\n"
    for header,value in request.headers.items():
        body += header + ": " + value + "\n"
    body += '\n\n'
    body += request.text
    return body

def URLENCODE(data):
    d = ''
    for word in data:
        d += '%' + binascii.b2a_hex(word.encode('utf-8')).decode('utf-8')
    return d

def urlencoder(data,many=1):
    for _ in range(many):
        data = URLENCODE(data)
    return data

def remove_dups(l):
    v = list()
    for i in l:
        if i not in v:
            v.append(i)
    return v

def remove_dups_urls(l):
    v = list()
    for i in l:
        if i not in v:
            if urlparse(i).netloc:
                v.append(i)
    return v

def insert_to_params_name(url,txt):
    out = list()
    try:
        for param in url.split('?')[1].split('&'):
            p = param.split('=')
            out.append(url.replace(p[0],p[0]+txt))
    except:
        return list()
    finally:
        return out

def force_insert_to_params_urls(url,txt):
    our = list()
    try:
        for param in url.split('?')[1].split('&'):
            our.append(url.replace(param,param.split('=')[0]+'='+txt))
        return our
    except:
        return list()
    finally:
        return our

def dump_params(url):
    return urlparse(url).query

def add_path(url,path):
    return urljoin(url,path)

def insert_to_params_urls(url,text,single=True,debug=False):
    u = list()
    try:
        if len(url.split('?')) >= 1:
            for param in url.split('?')[1].split('&'):
                u.append(url.replace(param,param + text))
        return remove_dups(u)
    except Exception as e:
        if debug:
            print(f'[insert_to_params_urls] {e}')
        return list()

def insert_to_params(param,text,single=True,debug=False):
    u = list()
    try:
        if len(param.split('&')) > 0:
            for p in param.split('&'):
                u.append(p.replace(p,p + text))
        return u
    except Exception as e:
        if debug:
            print(f'[insert_to_params] {e}')
        return u

def post_data(params,debug=False):
    try:
        if params:
            prePostData = params.split("&")
            postData = {}
            for d in prePostData:
                p = d.split("=", 1)
                postData[p[0]] = p[1]
            return postData
        return {}
    except Exception as e:
        if debug:
            print(e)
        return {}

def extractHeaders(headers='',debug=False):
    if headers:
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
            except Exception as e:
                if debug:
                    print ('[Extract Headers] {e}')
                return {}
        return sorted_headers
    return {}

def insertAfter(haystack, needle, newText):
  i = haystack.find(needle)
  return haystack[:i + len(needle)] + newText + haystack[i + len(needle):]
