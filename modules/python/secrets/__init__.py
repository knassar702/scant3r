#!/usr/bin/env python3
from .secrets import Scan

def main(opts, r):
    c = Scan(opts,r)
    c.start()
