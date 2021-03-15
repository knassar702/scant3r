#!/usr/bin/env python3

from modules import xss

class Scan:
    def __init__(self,opts):
        self.opts = {}
        self.scan = []
    def scan(self):
        xss.headers(self.opts['url'],methods=['GET'])
    def index(self):
        return 'hello :D'
def main(opts,r):
    v = Scan(opts)
    print(v)

