#!/usr/bin/env python3
from core.libs import show_error
from .lorsrf import Lorsrf

def main(opts, http):
    if opts['host']:
        Lorsrf(opts, http).start()
    else:
        show_error('lorsrf', 'Host not found')
        # (f'{bad} Host Not Found ..!') # -x option (ex: -x http://knassar702.burpcal.com)
