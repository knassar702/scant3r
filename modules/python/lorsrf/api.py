#!/usr/bin/env python3
from .lorsrf import Lorsrf
from core.libs import Http

def main(opts: dict, http: Http):
    if not opts['host']:
        return {'Lorsrf':'Error , add your host (-x)'}
    Lorsrf(opts , http).start()
    return {'Lorsrf':"Done :D"}
