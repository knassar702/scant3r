#!/usr/bin/env python3

from queue import Queue
from urllib.parse import urlparse as ur
from threading import Thread
from subprocess import call
from yaml import safe_load
from re import sub

class Start:
    def __init__(self,opts):
        self.op = dict()
        for op,va in opts.items():
            self.op[op] = va
        self.op['domain'] = ur(opts['url']).netloc
        self.mm = safe_load(open('modules/exec/conf.yaml','r'))
        self.opts = opts
        self.q = Queue()
    def execute(self,cmd):
        s = call(cmd.format(**self.op),shell=True)
        return s
    def threader(self):
        while True:
            item = self.q.get()
            self.execute(item)
            self.q.task_done()
    def run(self):
        for _ in range(self.opts['threads']):
            p1 = Thread(target=self.threader)
            p1.daemon = True
            p1.start()
        for p,v in self.mm.items():
            for m,c in v.items():
                self.q.put(c)
        self.q.join()
