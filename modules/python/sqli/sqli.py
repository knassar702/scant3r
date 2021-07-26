from core.libs import insert_to_params_urls, alert_bug, Http
from wordlists import sqli_payloads, sql_err
from urllib.parse import urlparse
from re import findall
from modules import Scan

class Sqli(Scan):
    def __init__(self, opts: dict, http: Http):
        super().__init__(opts, http)
        
    def start(self) -> dict:
        for method in self.opts['methods']:
            for payload in sqli_payloads:
                payload = payload.rstrip()
                new_url = insert_to_params_urls(self.opts['url'],payload)
                response = self.send_request(method, new_url)
                if type(response) == list:
                    return # connection error
                for err in sql_err:
                    err = err.rstrip()
                    if len(err.rstrip()) >= 1:
                        finder = findall(err,response.text)
                        for found in finder:
                            if found:
                                alert_bug('SQL injection', response, payload=urlparse(new_url).query,match=err)
        return {}
