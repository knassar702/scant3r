#!/usr/bin/env python3
from .paths import Paths

def main(opts,http):
    return Paths(opts, http).start()
