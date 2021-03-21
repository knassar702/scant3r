from urllib.parse import urlparse
from wordlists import ssti
from core.libs import insert_to_params_urls

class Scan:
    def __init__(self,opts,r):
        self.opts = opts
        self.http = r
    def scan(self,url,methods=['GET','POST']):
        for method in methods:
            for payload,match in ssti.items():
                nurl = insert_to_params_urls(url,payload)
                for n in nurl:
                    if method == 'GET':
                        r = self.http.send(method,n)
                    else:
                        r = self.http.send(method,url.split('?')[0],body=urlparse(n).query)
                    if match in r.content.decode('utf-8'):
                        print(f'''
[SSTI] {url.split("?")[0]}
    Method: {method}
    Params: {urlparse(n).query}
    Payload: {payload}
    Match: {match}
                            ''')
                        break


def main(opts,r):
    s = Scan(opts,r)
    s.scan(opts['url'],methods=opts['methods'])
