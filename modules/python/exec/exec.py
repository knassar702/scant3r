#!/usr/bin/env python3

from queue import Queue
from urllib.parse import urlparse as ur
from threading import Thread
from subprocess import call
from yaml import safe_load

q = Queue()

class Scan: 
    def __init__(self, opts):
        self.opts = opts
        self.op = self.define_op()
        
    def define_op(self):
        dict_op = dict()
        for op,va in self.opts.items():
            dict_op[op] = va 
        dict_op['domain'] = ur(self.opts['url']).netloc
        return dict_op
        
    def execute(self,cmd):
        s = call(cmd.format(**self.op),shell=True)
        return s
    
    def threader(self):
        while True:
            item = q.get()
            self.execute(item)
            q.task_done()
    
    def run(self):
        mm = safe_load(open(f'modules/python/exec/conf.yaml','r'))
        for _ in range(self.opts['threads']):
            p1 = Thread(target=self.threader)
            p1.daemon = True
            p1.start()
        for p,v in mm.items():
            for m,c in v.items():
                q.put(c)
        q.join()    