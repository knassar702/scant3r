#!/usr/bin/env python3
__author__ = 'Khaled Nassar'
__email__ = 'knassar702@gmail.com'
__version__ = '0.7#Beta'

from .colors import Colors as c
from .data import dump_request

def alert_bug(name,target,payload,match,http):
    print(f'''
{c.good} {c.red}{name}{c.rest}: {target.split("?")[0]}
    Method: {http.request.method}
    Payload: {payload}
    Match: {match}
---- Request ----
{c.yellow}
{dump_request(http).decode()}
{c.rest}
--------
''')
