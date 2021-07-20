#!/usr/bin/env python3
from .lorsrf import Lorsrf

def main(opts, http):
    if not opts['host']:
        return {'Lorsrf':'Error , add your host (-x)'}
    Lorsrf(opts , http).start()
    return {'Lorsrf':"Done :D"}
