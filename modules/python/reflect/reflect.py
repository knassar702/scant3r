from core.libs import insert_to_params_urls  as ur
from core.libs import random_str
from urllib.parse import urlparse

class Reflect:
    def __init__(self, opts, http):
        self.opts = opts
        self.http = http
        
    def start(self) -> list:
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