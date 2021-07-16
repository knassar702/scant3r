from core.libs import insert_to_params_urls, alert_bug
from wordlists import sqli_payloads,sql_err
from urllib.parse import urlparse
from re import findall
from queue import Queue
from threading import Thread


def start(op,http):
    for method in op['methods']:
        for payload in sqli_payloads:
            payload = payload.rstrip()
            n = insert_to_params_urls(op['url'],payload)
            for url in n:
                if method == 'GET':
                    r = http.send(method,url)
                else:
                    r = http.send(method,op['url'].split('?')[0],body=urlparse(url).query)
                for v in sql_err:
                    v = v.rstrip()
                    if len(v.rstrip()) >= 1:
                        hmm = findall(v,r.text)
                        for i in hmm:
                            if i:
                                alert_bug('SQL injection',r,payload=urlparse(url).query,match=v)
    return {}
def main(opts,r):
    c = start(opts,r)
    if c:
        return c
