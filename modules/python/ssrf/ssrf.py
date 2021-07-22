__author__ = 'Khaled Nassar'
__email__ = 'knassar702@gmail.com'
__version__ = '0.8#Beta'

from core.libs import alert_bug, dump_response, force_insert_to_params_urls, Http
from yaml import safe_load
from modules import Scan
import re

class Ssrf(Scan): 
    def __init__(self, opts: dict, http: Http):
        super().__init__(opts, http)
        
    def start(self) -> list: 
        conf = self.open_yaml_file("ssrf/payloads.yaml", True)
        for payload,match in conf.items():
            for method in self.opts['methods']:
                list_url = force_insert_to_params_urls(self.opts['url'],payload)
                for url in list_url:
                    vv = False
                    response = self.send_request(method, url, self.opts['url'])
                    
                    if match[1]['regex'] != False:
                        for i in match[0].values():
                            mm = i
                        c = re.compile(mm)
                        c = c.findall(dump_response(response))
                        if len(c) > 0:
                            vv = True
                    else:
                        for i in match[0].values():
                            mm = i
                        if mm in dump_response(response):
                            vv = True
                    if vv:
                        alert_bug('SSRF', response, POC=url)
        return []


