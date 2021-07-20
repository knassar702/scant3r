#!/usr/bin/env python3
from core.libs import show_error
from .lorsrf import Scan

def main(opts, http):
    if opts['host']:
        Scan(opts, http).scan()
    else:
        show_error('lorsrf', 'Host not found')
        # (f'{bad} Host Not Found ..!') # -x option (ex: -x http://knassar702.burpcal.com)
