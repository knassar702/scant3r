#!/usr/bin/env python3

__author__ = 'Khaled Nassar'
__email__ = 'knassar702@gmail.com'
__version__ = '0.7#Beta'

from threading import Thread
from queue import Queue
from libs import load_opts
import importlib,sys

q = Queue()

def Get(name):
    name = f'modules.active.{name}'
    try:
        c = importlib.import_module(name)
        return c
    except Exception as e:
        print(e)
        sys.exit()
class Import:
    def threader(func):
        while True:
            item = q.get()
            func.main(item)
            q.task_done()
    def run(func):
        opts = load_opts()
        for i in range(opts['threads']):
            p1 = Thread(target=Import.threader,args=(func,))
            p1.daemon = True
            p1.start()
        for url in opts['url']:
            n = load_opts()
            n['url'] = url
            q.put(n)
        q.join()
