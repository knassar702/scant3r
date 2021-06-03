from core.libs import insert_to_params_urls
from wordlists import sqli_payloads,sql_err
from urllib.parse import urlparse
from re import findall
from queue import Queue
from threading import Thread


def start(op,http):
    for method in op['methods']:
        for payload in sqli_payloads:
            n = insert_to_params_urls(op['url'],payload)
            for url in n:
                if method == 'GET':
                    r = http.send(method,url)
                else:
                    r = http.send(method,op['url'].split('?')[0],body=urlparse(url).query)
                for v in sql_err:
                    if len(v) > 0:
                        hmm = findall(v,r.content.decode('utf-8'))
                        for i in hmm:
                            if i:
                                return {
                                    'method':method,
                                    'url':url.split('?')[0],
                                    'params':urlparse(url).query,
                                    'payload':payload,
                                    'match':v
                                    }
    return {}
def main(opts,r):
    c = start(opts,r)
    if c:
        print(f'''[SQLI] {c["url"]}
\tParams: {c["params"]}
\tMethod: {c["method"]}
\tPayload: {c["payload"]}
\tMatch: {c["match"]}
                ''')
