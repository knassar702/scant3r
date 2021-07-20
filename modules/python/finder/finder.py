from yaml import safe_load
from re import findall
from core.libs import dump_request, dump_response
from urllib.parse import urlparse

class Scan: 
    def __init__(self, opts, http):
        self.opts = opts 
        self.http = http
        
    def scan(self):
        f = safe_load(open('modules/python/finder/find.yaml','r'))
        found = dict()
        
        for method in self.opts['methods']:
            
            if method == 'GET':
                r = self.http.send(method, self.opts['url'])
            else: 
                r = self.http.send(method, self.opts['url'].split('?')[0], body=urlparse(self.opts['url']).query)
                
            for name, data in f.items(): 
                hm = {}
                
                for i in data: 
                    for v,vv in i.items():
                        hm[v] = v
                
                if 'part' in hm.keys():
                    if hm['part'] == 'request':
                        part = dump_request(r)
                    else: 
                        part = dump_response(r)
                else : 
                    part = dump_response(r)
                    
                if hm['regex']: 
                    m = findall(hm['text'], part)
                    for ff in m: 
                        if ff: 
                            found[name] = {
                                'find': name, 
                                'http': r,
                                'method': method,
                                'match': hm['text'],
                                'regex': False
                            }
                else: 
                    if hm['text'] in part:
                        found[name] = {
                            'find': name, 
                            'http': r,
                            'method': method,
                            'match': hm['text'],
                            'regex': False
                        }
        return found