from yaml import safe_load
from re import findall
from core.libs import dump_request,dump_response
from urllib.parse import urlparse

def start(op,http):
    f = safe_load(open('modules/finder/find.yaml','r'))
    found = {}
    for method in op['methods']:
        url = op['url']
        if method == 'GET':
            r = http.send(method,url)
        else:
            r = http.send(method,url.split('?')[0],body=urlparse(url).query)
        for name,data in f.items():
            hm = {}
            for i in data:
                for v,vv in i.items():
                    hm[v] = vv
            if 'part' in hm.keys():
                if hm['part'] == 'request':
                    part = dump_request(r).decode()
                else:
                    part = dump_response(r).decode()
            else:
                part = dump_response(r).decode()
            if hm['regex']:
                m = findall(hm['text'],part)
                for ff in m:
                    if ff:
                        found[name] = {
                                'target':url.split('?')[0],
                                'params':urlparse(url).query,
                                'method':method,
                                'match':hm["text"],
                                'regex':m,
                                }
                        print(f'[FINDER] :> {name}\n\tTarget: {url.split("?")[0]}\n\tParams: {urlparse(url).query}\n\tMethod: {method}\n\tMatch: {hm["text"]}\n\rRegex: {m}\n---')
            else:
                if hm['text'] in part:
                    found[name] = {
                                'target':url.split('?')[0],
                                'params':urlparse(url).query,
                                'method':method,
                                'match':hm["text"],
                                'regex':False
                            }
                    print(f'[FINDER] :> {name}\n\tTarget: {url.split("?")[0]}\n\tParams: {urlparse(url).query}\n\tMethod: {method}\n\tMatch: {hm["text"]}\n\t---')
    return found
def main(opts,r):
    start(opts,r)
