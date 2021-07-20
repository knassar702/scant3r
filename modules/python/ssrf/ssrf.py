__author__ = 'Khaled Nassar'
__email__ = 'knassar702@gmail.com'
__version__ = '0.8#Beta'

from core.libs import alert_bug, dump_response, force_insert_to_params_urls
from urllib.parse import urlparse # url parsing
from yaml import safe_load
import re
from scan import Scan
class Ssrf(Scan): 
    def __init__(self, opts, http):
        super().__init__(opts, http)
        
    def start(self): 
        conf = safe_load(open('modules/python/ssrf/payloads.yaml'))
        for payload,match in conf.items():
            for method in self.opts['methods']:
                list_url = force_insert_to_params_urls(self.opts['url'],payload)
                for nurl in list_url:
                    vv = False
                    if method == 'GET':
                        r = self.http.send(method,nurl)
                    else:
                        r = self.http.send(method, self.opts['url'].split('?')[0],body=urlparse(nurl).query)
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


