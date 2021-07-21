from core.libs import insert_to_params_urls  as ur
from core.libs import random_str, Http
from urllib.parse import urlparse
from scan import Scan
from typing import Union

class Reflect(Scan):
    def __init__(self, opts: dict, http: Http):
        super().__init__(opts, http)
        
    def start(self) -> Union[list,dict]:
        found = dict()
        txt = f'scan{random_str(3)}tr'
        
        for method in self.opts['methods']:
            if urlparse(self.opts['url']).query:
                nurls = ur(self.opts['url'],txt)
            else:
                return []
            for nurl in nurls:
                if method == 'GET':
                    r = self.http.send(method,nurl)
                else:
                    r = self.http.send(method,nurl.split('?')[0],body=urlparse(nurl).query)
                if txt in r.text:
                    found = method
  
        return found