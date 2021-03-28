#!/usr/bin/env python3

from .lorsrf import start

def main(opts,http):
    host = opts['host']
    if host:
            start(opts,http)
    else:
        # (f'{bad} Host Not Found ..!') # -x option (ex: -x http://knassar702.burpcal.com)
        return
