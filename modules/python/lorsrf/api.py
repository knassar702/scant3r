#!/usr/bin/env python3
from .lorsrf import start

def main(opts,msg):
    if opts['host']:
        pass
    else:
        return {'Lorsrf':'Error , add your host (-x)'}
    start(opts['url'],opts['host'],msg)
    return {'Lorsrf':"Done :D"}
