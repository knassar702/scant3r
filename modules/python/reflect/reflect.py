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
            if not urlparse(self.opts['url']).query:
                return []
            
            list_url = ur(self.opts['url'],txt)
            
            for url in list_url:
                response = self.send_request(method, url)
                
                if txt in response.text:
                    found = method
  
        return found