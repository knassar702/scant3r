from wordlists import rce_payloads
from core.libs import insert_to_params_urls, alert_bug ,dump_response, Http
from urllib.parse import urlparse
from modules import Scan

class Rce(Scan):
    def __init__(self, opts: dict, http: Http):
        super().__init__(opts, http)
        
    def start(self) -> dict:
        for method in self.opts['methods']:
            for payload,match in rce_payloads().items():
                new_url = insert_to_params_urls(self.opts['url'],payload.replace('\n','%0a').replace('\t','%0d'))
                response = self.send_request(method, new_url)
                if type(response) == list:
                    return # connection error
                if match in dump_response(response):
                    alert_bug('RCE',response,payload=payload,match=match)
                    break
        return {}
