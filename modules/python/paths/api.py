#!/usr/bin/env python3
from .paths import Paths
from core.libs import Http

def main(opts: dict, http: Http):
    return Paths(opts, http).start()
