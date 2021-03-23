from wordlists import rce_payloads
from core.libs import dump,insert_to_params_urls
from urllib.parse import urlparse

def scan(http,url,methods=['GET','POST']):
    for method in methods:
        for payload,match in rce_payloads.items():
            nurl = insert_to_params_urls(url,payload.replace('\n','%0a').replace('\t','%0d'))
            for u in nurl:
                if method == 'GET':
                    r = http.send(method,u)
                else:
                    r = http.send(method,u.split('?')[0],body=urlparse(u).query)
                if r != 0: # 0 = connection error
                    if match in dump.dump_all(r).decode('utf-8'):
                        return {
                                'method':method,
                                'target':url.split('?')[0],
                                'params':urlparse(u).query,
                                'payload':payload.replace('\n','%0a').replace('\t','%0d'),
                                'match':match
                                }
    return {}
def main(opts,r):
    s = scan(r,opts['url'],opts['methods'])
    if s:
        print(f'[Remote Code Execution] {s["target"]}\n\tMethod: {s["method"]}\n\tParams: {s["params"]}\n\tPayload: {s["payload"]}\n\tMatch: {s["match"]}')
