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
            item[1]['url'] = item[0]
            c.main(item[1])
            q.task_done()
    def run(opts):
        for i in range(opts['threads']):
            p1 = Thread(target=Import.threader)
            p1.daemon = True
            p1.start()
        for url in opts['url']:
            q.put(handeropts(url,opts))
        q.join()
