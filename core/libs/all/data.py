#!/usr/bin/env python3
__author__ = 'Khaled Nassar'
__email__ = 'knassar702@gmail.com'
__version__ = '0.8#Beta'

import re
import binascii
import random
import logging
import string
from urllib.parse import urljoin, urlparse , urlencode , urlunparse ,urlunparse , parse_qsl
from requests.models import Response
from .colors import *

log = logging.getLogger('scant3r')

# Generate a random string. Arg int return str 
def random_str(num: int) -> str:
    num = int(num)
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(num))


# Print the request in the console. Arg the request. Return a string. Empty string if no request
def dump_request(request : Response) -> str:
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

# Print the response in the console. Arg the request. Return a string. Empty string if no response
def dump_response(request : Response) -> str:
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

# from plain text to url encoding
def urlencoder(data, many=1):
    for _ in range(many):
        data = URLENCODE(data)
    return data

# Remove duplicate element from a list. Arg List return a clean list
def remove_dups(l: list) -> list:
    v = list()
    [ v.append(x) for x in l if x not in v ]
    return v

# Remove duplicate url from a list. Arg list of url. Return a clean Url list
def remove_dups_urls(l : list) -> list:
    v = list()
    [ v.append(i) for i in l if i not in v and urlparse(i).netloc ]
    return v

# Insert param 
def insert_to_params_name(url: str, text: str) -> list:
    try:
        parse_url = urlparse(url)
        query = parse_url.query
        url_dict = dict(parse_qsl(query))
        for param,value in url_dict.copy().items():
            new_param = param + text
            url_dict.pop(param)
            url_dict[new_param] = value
        new_url = urlencode(url_dict)
        parse_url = parse_url._replace(query=new_url)
        return urlunparse(parse_url)
    except Exception as e :
        log.error(e)
        return []

# Insert param to custom parameter name
def insert_to_custom_params(url: str,parameter: str, text: str, remove_content: bool = False) -> str:
    try:
        parse_url = urlparse(url)
        query = parse_url.query
        url_dict = dict(parse_qsl(query))
        if parameter not in url_dict:
            log.debug('cant find the parameter')
            return url
        for param,value in url_dict.copy().items():
            if remove_content:
                url_dict[param] = text
            url_dict[param] = value + text
        new_url = urlencode(url_dict)
        parse_url = parse_url._replace(query=new_url)
        return urlunparse(parse_url)
    except Exception as e:
        log.error(e)
        return url

# Return the query from the url 
def dump_params(url: str):
    return urlparse(url).query

# Add a path to an url
def add_path(url: str, path: str) -> str:
    return urljoin(url,path)

# Add a string to url parameters
def insert_to_params_urls(url: str, text: str, remove_content: bool = False) -> list :
    try:
        parse_url = urlparse(url)
        query = parse_url.query
        url_dict = dict(parse_qsl(query))
        for param,value in url_dict.copy().items():
            if remove_content:
                url_dict[param] = text
            url_dict[param] = value + text
        new_url = urlencode(url_dict)
        parse_url = parse_url._replace(query=new_url)
        return urlunparse(parse_url)
    except Exception as e:
        log.debug(e)
        return list()

# add parameters to url 
def insert_to_params(param: str, text: str, debug : bool=False) -> str:
    u = list()
    try:
        if len(param.split('&')) > 0:
            for p in param.split('&'):
                u.append(p.replace(p,p + text))
        return u
    except Exception as e:
        log.debug(e)
        return u

# add string value to dictionary (for cookies,post/put parameters)
def post_data(params: str, debug: bool = False) -> dict:
    try:
        if '?' not in params or '&' not in params:
            return {}
        if params:
            prePostData = params.split("&")
            postData = {}
            for d in prePostData:
                p = d.split("=", 1)
                postData[p[0]] = p[1]
            return postData
        return {}
    except Exception as e:
        log.debug(e)
        return {}

# Convert string headers to a dict Headers
def extract_headers(headers: str = '', debug: bool =False) -> dict:
    try:
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
                    log.debug(e)
                    return {}
            return sorted_headers
        return {}
    except Exception as e:
        log.debug(e)
        return {}
    
# Convert cookie string to a dict 
def extract_cookie(cookies: str)-> dict: 
    dict_cookies = {}
    if cookies: 
        cookies = cookies.strip()
        list_cookie = cookies.split(';')
        for cookie in list_cookie: 
            cookie = cookie.strip()
            list_value_name_cookie = cookie.split('=')
            dict_cookies[list_value_name_cookie[0].strip()] = list_value_name_cookie[1].strip()
            
    return dict_cookies          
    
#  Insert some string into given string at given index
def insert_after(text: str, find_this: str, newText: str) -> str:
  i = text.find(find_this)
  return text[:i + len(find_this)] + newText + text[i + len(find_this):]
