from wordlists import rce_payloads
from core.libs import insert_to_params_urls ,dump_response, Http
from urllib.parse import urlparse
from modules import Scan

class Rce(Scan):
    def __init__(self, opts: dict, http: Http):
        super().__init__(opts, http)
        
    def start(self) -> dict:
        for method in self.opts['methods']:
            for payload,match in rce_payloads().items():
                nurl = insert_to_params_urls(self.opts['url'],payload.replace('\n','%0a').replace('\t','%0d'))
                for u in nurl:
                    if method == 'GET':
                        r = self.http.send(method,u)
                    else:
                        r = self.http.send(method,u.split('?')[0],body=urlparse(u).query)
                    if r != 0: # 0 = connection error
                        if match in dump_response(r):
                            return {
                                'payload':payload.replace('\n','%0a').replace('\t','%0d'),
                                'match':match,
                                'http':r
                            }
        return {}
