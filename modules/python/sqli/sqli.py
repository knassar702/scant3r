from core.libs import insert_to_params_urls, alert_bug, Http
from wordlists import sqli_payloads, sql_err
from urllib.parse import urlparse
from re import findall
from modules import Scan

class Sqli(Scan):
    def __init__(self, opts: dict, http: Http):
        super().__init__(opts, http)
        
    def start(self) -> list:
        for method in self.opts['methods']:
            for payload in sqli_payloads:
                payload = payload.rstrip()
                list_url = insert_to_params_urls(self.opts['url'],payload)
                for url in list_url:
                    response = self.send_request(method, url, self.opts['url'])
                    for v in sql_err:
                        v = v.rstrip()
                        if len(v.rstrip()) >= 1:
                            hmm = findall(v,response.text)
                            for i in hmm:
                                if i:
                                    alert_bug('SQL injection', response, payload=urlparse(url).query,match=v)
        return {}
