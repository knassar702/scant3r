from core.libs import insert_to_params_urls, alert_bug
from wordlists import sqli_payloads, sql_err
from urllib.parse import urlparse
from re import findall

class Scan:
    def __init__(self, opts, r):
        self.opts = opts
        self.http = r
        
    def scan(self):
        for method in self.opts['methods']:
            for payload in sqli_payloads:
                payload = payload.rstrip()
                n = insert_to_params_urls(self.opts['url'],payload)
                for url in n:
                    if method == 'GET':
                        r = self.http.send(method,url)
                    else:
                        r = self.http.send(method,self.opts['url'].split('?')[0],body=urlparse(url).query)
                    for v in sql_err:
                        v = v.rstrip()
                        if len(v.rstrip()) >= 1:
                            hmm = findall(v,r.text)
                            for i in hmm:
                                if i:
                                    alert_bug('SQL injection',r,payload=urlparse(url).query,match=v)
        return {}