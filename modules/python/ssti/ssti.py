from wordlists import ssti_payloads as ssti
from core.libs import insert_to_params_urls, Http
from modules import Scan
class Ssti(Scan):
    def __init__(self, opts: dict, http: Http):
        super().__init__(opts, http)
    
    def start(self):
        for method in self.opts['methods']:
            for payload,match in ssti().items():
                list_url = insert_to_params_urls(self.opts['url'],payload)
                for url in list_url:
                    response = self.send_request(method, url, self.opts['url'])
                    # 0 = Connection error:
                    if response != 0 and match in response.text: 
                        return {
                            'http': response,
                            'target': url,
                            'match': match,
                            'payload': payload,
                        }
