from yaml import safe_load
from re import findall
from core.libs import dump
from urllib.parse import urlparse

def start(op,http):
    f = safe_load(open('modules/finder/find.yaml','r'))
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
            if hm['regex']:
                m = findall(hm['text'],dump.dump_all(r).decode('utf-8'))
                for ff in m:
                    if ff:
                        print(f'[FINDER] :> {name}\n\tTarget: {url.split("?")[0]}\n\tParams: {urlparse(url).query}\n\tMethod: {method}\n\tMatch: {hm["text"]}\n\rRegex: {m}\n---')
            else:
                if hm['text'] in dump.dump_all(r).decode('utf-8'):
                    print(f'[FINDER] :> {name}\n\tTarget: {url.split("?")[0]}\n\tParams: {urlparse(url).query}\n\tMethod: {method}\n\tMatch: {hm["text"]}\n\t---')
def main(opts,r):
    start(opts,r)
