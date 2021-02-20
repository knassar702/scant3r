#!/usr/bin/env python3

__author__ = 'Khaled Nassar'
__email__ = 'knassar702@gmail.com'
__version__ = '0.6#Beta'

from threading import Thread
from queue import Queue
import importlib,sys

q = Queue()

def handeropts(url,options):
    return url,options
class Import:
    def Get(name):
        global c
        name = f'modules.active.{name}'
        try:
            c = importlib.import_module(name)
            return c
        except Exception as e:
            print(e)
            sys.exit()
    def threader():
        while True:
            item = q.get()
            c.main(item)
            q.task_done()
    def save():
        global opt
        opt = {}
    def run(opts):
        global opt
        Import.save()
        for o,v in opts.items():
            opt[o] = v
        for i in range(opts['threads']):
            p1 = Thread(target=Import.threader)
            p1.daemon = True
            p1.start()
        for url in opt['url']:
            opt['url'] = url
            q.put(opt)
        q.join()
