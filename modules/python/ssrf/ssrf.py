__author__ = 'Khaled Nassar'
__email__ = 'knassar702@gmail.com'
__version__ = '0.8#Beta'

from core.libs import alert_bug, dump_response, insert_to_params_urls , Http
from yaml import safe_load
from modules import Scan
import re

class Ssrf(Scan): 
    def __init__(self, opts: dict, http: Http):
        super().__init__(opts, http)
        
    def start(self) -> list: 
        found = {}
        conf = self.open_yaml_file("ssrf/payloads.yaml", True)
        for payload,match in conf.items():
            for method in self.opts['methods']:
                new_url = insert_to_params_urls(self.opts['url'],payload,True)
                response = self.send_request(method, new_url)
                if match[1]['regex'] != False:
                    for match_value in match[0].values():
                        c = re.compile(match_value)
                        c = c.findall(dump_response(response))
                        if len(c) > 0:
                            found = {'match':match_value,'regex':True}
                else:
                    for match_value in match[0].values():
                        if match_value in dump_response(response):
                            found = {'match':match_value,'regex':False}
                            break
                if found:
                    alert_bug('SSRF', response, payload=payload,**found)
        return []


