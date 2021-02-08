#!/usr/bin/env python3
from libs import NewRequest as nq
from urllib.parse import urljoin
from core import good

"""
paths = {
  "/PATH":"MESSAGE",
  "/PATH2":200 # status code
    }
"""




paths = {
    '/phpinfo.php':'PHP Version',
    '/PI.php':'PHP Version',
    '/+CSCOT+/translation-table?type=mst&textdomain=/%2bCSCOE%2b/portal_inc.lua&default-language&lang=../':'dofile("',
    '/pluto/portal':'<title>Pluto Portal</title>'
        }








def GO(host):
    h = host
    for path,msg in paths.items():
        host = urljoin(host,path)
        try:
            r = nq.Get(host)
            if r != 0:
                try:
                    int(msg)
                    if msg == r.status_code:
                        print(f'{good} Found :> {host}')
                except:
                    if msg in r.content.decode('utf-8'):
                        print(f'{good} Found :> {host}')
        except:
            pass
        finally:
            host = h

def main(opts):
    GO(opts['url'])
