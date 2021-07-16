__author__ = 'Khaled Nassar'
__email__ = 'knassar702@gmail.com'
__version__ = '0.7#Beta'

from core.libs import alert_bug,post_data,urlencoder,dump_response,force_insert_to_params_urls
from urllib.parse import urlparse # url parsing
from yaml import safe_load
import re

def start(opts,url,http,methods=['GET','POST']):
    conf = safe_load(open('modules/ssrf/payloads.yaml'))
    for payload,match in conf.items():
        for method in methods:
            v = force_insert_to_params_urls(url,payload)
            for nurl in v:
                vv = False
                if method == 'GET':
                    r = http.send(method,nurl)
                else:
                    r = http.send(method,url.split('?')[0],body=urlparse(nurl).query)
                if match[1]['regex'] != False:
                    for i in match[0].values():
                        mm = i
                    c = re.compile(mm)
                    c = c.findall(dump_response(r))
                    if len(c) > 0:
                        vv = True
                else:
                    for i in match[0].values():
                        mm = i
                    if mm in dump_response(r):
                        vv = True
                if vv:
                    alert_bug('SSRF',r,POC=nurl)
    return []
