from urllib.parse import urlparse
from core.libs import alert_bug , random_str, urlencoder, insert_to_params_name, Http
from wordlists import XSS
from modules import Scan
class XssParam(Scan):
    def __init__(self, opts: dict, http: Http):
        super().__init__(opts, http)
        self.payloads = XSS(opts['blindxss']).payloads
        
    def reflect(self, url: str, method: str ='GET') -> list:
        ref = []
        txt = f'scan{random_str(2)}'
        url = insert_to_params_name(url,txt)
        response = self.send_request(method, url)
        if type(response) == list:
            return [] # connection error
        if txt in response.text:
            ref.append(txt)
        return ref
    
    def start(self) -> dict:
        for method in self.opts['methods']:
            reflected = self.reflect(self.opts['url'],method=method)
            if len(reflected) > 0:
                for payload in self.payloads:
                    payload = payload.rstrip()
                    nurl = insert_to_params_name(self.opts['url'],urlencoder(payload))
                    response = self.send_request(method, nurl)
                    if payload in response.text:
                        alert_bug('XSS PARAMETER NAME',response,payload=payload)
