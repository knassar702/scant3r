from yaml import safe_load
from re import findall
from core.libs import alert_bug,remove_dups,dump_request,dump_response
from urllib.parse import urlparse

def start(op,http):
    f = safe_load(open('modules/finder/find.yaml','r'))
    found = dict()
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
                                'find':name,
                                'http':r,
                                'match':hm["text"],
                                'regex':m
                                }
            else:
                if hm['text'] in part:
                    found[name] = {
                                'find':name,
                                'http':r,
                                'method':method,
                                'match':hm["text"],
                                'regex':False
                                }
    return found
def main(opts,r,api=False):
    v = start(opts,r)
    if v:
        for i,c in v.items():
            alert_bug('FINDER',**c)
        if api:
            return v
