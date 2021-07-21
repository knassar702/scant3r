from urllib.parse import urlparse
from core.libs import random_str, urlencoder, insert_to_params_name, Http
from wordlists import XSS
from modules import Scan
class XssParam(Scan):
    def __init__(self, opts: dict, http: Http):
        super().__init__(opts, http)
        self.payloads = XSS(opts['blindxss']).payloads
        
    def reflect(self, url: str, method: str ='GET') -> list:
        ref = []
        txt = f'scan{random_str(2)}'
        for u in insert_to_params_name(url,txt):
            response = self.send_request(method, u)
            if response != 0 and txt in response.text:
                ref.append(txt)
        return ref
    
    def start(self):
        for method in self.opts['methods']:
            v = self.reflect(self.opts['url'],method=method)
            if len(v) > 0:
                for payload in self.payloads:
                    payload = payload.rstrip()
                    for nurl in insert_to_params_name(self.opts['url'],urlencoder(payload)):
                        response = self.send_request(method, nurl, self.opts['url'])
                        if response != 0 and payload in response.text:
                            print(f'[XSS Parameter Name: {method}] :> {nurl}\n')
                            return {method:nurl}
