from wordlists import ssti_payloads as ssti
from core.libs import insert_to_params_urls, alert_bug ,Http
from modules import Scan



class Ssti(Scan):
    def __init__(self, opts: dict, http: Http):
        super().__init__(opts, http)
    
    def start(self) -> dict:
        for method in self.opts['methods']:
            for payload,match in ssti().items():
                new_url = insert_to_params_urls(self.opts['url'],payload)
                response = self.send_request(method, new_url, self.opts['url'])
                if type(response) != list: # 0 = Connection error:
                    if match in response.text: 
                        alert_bug('SSTI',response,payload=payload,match=match)
        return {}
