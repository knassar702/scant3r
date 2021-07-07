from wordlists import rce_payloads
from core.libs import alert_bug,insert_to_params_urls,dump_request,dump_response
from urllib.parse import urlparse

def scan(http,url,methods=['GET','POST']):
    for method in methods:
        for payload,match in rce_payloads().items():
            nurl = insert_to_params_urls(url,payload.replace('\n','%0a').replace('\t','%0d'))
            for u in nurl:
                if method == 'GET':
                    r = http.send(method,u)
                else:
                    r = http.send(method,u.split('?')[0],body=urlparse(u).query)
                if r != 0: # 0 = connection error
                    if match in dump_response(r).decode('utf-8'):
                        return {
                                'payload':payload.replace('\n','%0a').replace('\t','%0d'),
                                'match':match,
                                'http':r
                                }
    return {}
def main(opts,r):
    s = scan(r,opts['url'],opts['methods'])
    if s:
        alert_bug('Remote Code Execution',**s)
