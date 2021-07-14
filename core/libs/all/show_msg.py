#!/usr/bin/env python3
__author__ = 'Khaled Nassar'
__email__ = 'knassar702@gmail.com'
__version__ = '0.8#Beta'

from .colors import Colors as c
from .data import dump_request
from urllib.parse import urlparse 
from os.path import splitext,isfile
from os import mkdir
import random,re

def alert_bug(name,http,**kwargs):
    f = f'{c.good} {c.red}{name}{c.rest}: {http.request.url.split("?")[0]}'
    f += f'\n  Method: {http.request.method}'
    vv = ''

    for p,v in kwargs.items():
        vv += f'\n  {p}: {v}'
    f += vv
    f += f'''
---- Request ----
{c.yellow}
{dump_request(http)}
{c.rest}
--------
'''
    target = urlparse(http.request.url).netloc
    print(f)
    if isfile(f'log/{target}') == True:
        mkdir(f'log/{target}')
    ooo = open(f'log/{target}/{name}_{random.randint(1,100)}.txt','w')
    f = re.compile(r'''
    \x1B  # ESC
    (?:   # 7-bit C1 Fe (except CSI)
        [@-Z\\-_]
    |     # or [ for CSI, followed by a control sequence
        \[
        [0-?]*  # Parameter bytes
        [ -/]*  # Intermediate bytes
        [@-~]   # Final byte
    )
''', re.VERBOSE).sub('',f)
    ooo.write(f)
    ooo.close()
    return {'Name':name,
            'request':dump_request(http),
            'output':kwargs
            }
