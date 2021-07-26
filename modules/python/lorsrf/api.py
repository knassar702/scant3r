#!/usr/bin/env python3
from .lorsrf import Lorsrf
from core.libs import Http

def main(opts: dict, http: Http):
    Lorsrf(opts , http).start()
