from core.libs import alert_bug , random_str, Http, insert_text_to_urlpath, insert_to_params_urls 
from logging import getLogger
from modules import Scan

log = getLogger('scant3r')

class Reflect(Scan):
    def __init__(self, opts: dict, http: Http):
        super().__init__(opts, http)
        
    def start(self) -> dict:
        txt = f'scan{random_str(3)}tr'
        for method in self.opts['methods']:
            paths = insert_text_to_urlpath(self.opts['url'],txt)
            new_url = insert_to_params_urls(self.opts['url'],txt)
            response = self.send_request(method, new_url)
            if txt in response.text:
                alert_bug('Reflect',response,match=txt,location='URL Parameters')
            for path in paths:
                response = self.send_request(method,path)
                if txt in response.text:
                    alert_bug('Reflect',response,match=txt,location='URL Path')
        return {}
