#!/usr/bin/env python3
from urllib.parse import urljoin
from core.libs import Colors as c
from yaml import safe_load


def start(host,http):
    h = host
    found = []
    f = safe_load(open('modules/python/paths/conf.yaml','r'))
    for path,msg in f.items():
        host = urljoin(host,path)
        try:
            r = http.send('GET',host)
            if r != 0:
                try:
                    int(msg)
                    if msg == r.status_code:
                        print(f'{c.good} Found :> {host}')
                        found.append(host)
                except:
                    if msg in r.text:
                        print(f'{c.good} Found :> {host}')
                        found.append(host)
        except:
            pass
        finally:
            host = h
    return found
