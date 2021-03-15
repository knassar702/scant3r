#!/usr/bin/env python3

__author__ = 'Khaled Nassar'
__email__ = 'knassar702@gmail.com'
__version__ = '0.7#Beta'

import importlib
import concurrent.futures

class MLoader:
    def __init__(self):
        self.thr = list()
        self.modules = list()
    def get(self,name):
        name = f'modules.{name}'
        try:
            c = importlib.import_module(name)
            self.modules.append(c)
            return c
        except Exception as e:
            print(e)
    def run(self,opts,r):
        opt = opts.copy() # copy user options
        print(f'Modules Loaded :> {len(self.modules)}')
        with concurrent.futures.ThreadPoolExecutor(max_workers=opts['threads']) as executor:
            for url in opts['urls']:
                opt['url'] = url
                for module in self.modules:
                    if module.main.__code__.co_argcount >= 2:
                        c = executor.submit(module.main, opt,r)
                        print(c.result())
                    else:
                        executor.submit(module.main,opt)
                opt = opts.copy()
