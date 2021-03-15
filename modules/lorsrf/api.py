#!/usr/bin/env python3
from .lorsrf import start

def main(url,opts,msg):
    if opts['host']:
        pass
    else:
        return {'Lorsrf':'Error , add your host (-x)'}
    start(url,opts['host'],msg)
    return {'Lorsrf':"Done :D"}
