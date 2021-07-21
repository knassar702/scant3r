#!/usr/bin/env python3
from core.libs import show_error, Http
from .lorsrf import Lorsrf

def main(opts: dict, http: Http):
    if opts['host']:
        Lorsrf(opts, http).start()
    else:
        show_error('lorsrf', 'Host not found')
        # (f'{bad} Host Not Found ..!') # -x option (ex: -x http://knassar702.burpcal.com)
