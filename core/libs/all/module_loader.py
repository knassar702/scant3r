#!/usr/bin/env python3

__author__ = 'Khaled Nassar'
__email__ = 'knassar702@gmail.com'
__version__ = '0.7#Beta'

import importlib
import concurrent.futures

class MLoader:
    def __init__(self):
        self.thr = list()
        self.modules = dict()
    def get(self,name):
        name = f'modules.{name}'
        try:
            c = importlib.import_module(name)
            self.modules[name] = c
            return c
        except Exception as e:
            print(e)
    def run(self,opts,r):
        opt = opts.copy() # copy user options
        with concurrent.futures.ThreadPoolExecutor(max_workers=opts['threads']) as executor:
            mres = []
            for url in opts['urls']:
                opt['url'] = url
                for n,module in self.modules.items():
                    if module.main.__code__.co_argcount >= 2:
                        mres.append(executor.submit(module.main, opt,r))
                    else:
                        mres.append(executor.submit(module.main,opt))
                opt = opts.copy()
            for future in concurrent.futures.as_completed(mres):
                res = future.result()
                if res:
                    print(res)
