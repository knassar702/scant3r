#!/usr/bin/env python3

from queue import Queue
from urllib.parse import urlparse as ur
from threading import Thread
from subprocess import call
from logging import getLogger
from yaml import safe_load
from modules import Scan
from core.libs import Http

q = Queue()
log = getLogger('scant3r')

class Exec(Scan): 
    def __init__(self, opts: dict, http: Http):
        super().__init__(opts, http)
        self.op = self.define_op()
        
    def define_op(self):
        dict_op = dict()
        for op,va in self.opts.items():
            dict_op[op] = va 
        dict_op['domain'] = ur(self.opts['url']).netloc
        return dict_op
        
    def execute(self,cmd):
        log.info(f'Execute {cmd}')
        s = call(cmd.format(**self.op),shell=True)
        return s
    
    def threader(self):
        while True:
            item = q.get()
            self.execute(item)
            q.task_done()
    
    def start(self):
        log.debug('load exec conf file')
        mm = self.open_yaml_file('exec/conf.yaml', True)
        for _ in range(self.opts['threads']):
            log.debug('new thread started')
            p1 = Thread(target=self.threader)
            p1.daemon = True
            p1.start()
        for p,v in mm.items():
            for m,c in v.items():
                q.put(c)
        q.join()    
