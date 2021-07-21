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
                list_url = insert_to_params_urls(self.opts['url'],payload.replace('\n','%0a').replace('\t','%0d'))
                for url in list_url:
                    response = self.send_request(method, url)
                    # 0 = connection error
                    if response != 0 and match in dump_response(response): 
                        return {
                            'payload':payload.replace('\n','%0a').replace('\t','%0d'),
                            'match':match,
                            'http':response
                        }
        return {}
