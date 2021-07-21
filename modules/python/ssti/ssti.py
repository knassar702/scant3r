from wordlists import ssti_payloads as ssti
from urllib.parse import urlparse
from core.libs import insert_to_params_urls, Http
from modules import Scan
class Ssti(Scan):
    def __init__(self, opts: dict, http: Http):
        super().__init__(opts, http)
    
    def start(self):
        for method in self.opts['methods']:
            for payload,match in ssti().items():
                nurl = insert_to_params_urls(self.opts['url'],payload)
                for n in nurl:
                    if method == 'GET':
                        r = self.http.send(method,n)
                    else:
                        r = self.http.send(method, self.opts['url'].split('?')[0], body=urlparse(n).query)
                    if r != 0: # 0 = Connection error:
                        if match in r.text:
                            return {
                                'http':r,
                                'target':n,
                                'match':match,
                                'payload':payload,
                            }
