#!/usr/bin/env python3

from .lorsrf import start

def main(opts,http):
    host = opts['host']
    if host == None:
        # (f'{bad} Host Not Found ..!') # -x option (ex: -x http://knassar702.burpcal.com)
        return
    else:
        for method in opts['methods']:
            start(opts['url'],host,http,methods=[method])
