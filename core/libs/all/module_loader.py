#!/usr/bin/env python3

__author__ = 'Khaled Nassar'
__email__ = 'knassar702@gmail.com'
__version__ = '0.7#Beta'

import importlib
import concurrent.futures
import yaml
from urllib.parse import urlparse as ur
from os.path import splitext,isfile
import subprocess

class MLoader:
    def __init__(self):
        self.thr = list()
        self.modules = dict()
        self.lang = yaml.safe_load(open('core/settings/lang.yaml','r'))
    def get(self,name):
        try:
            c = None
            run = False
            if len(splitext(name)[1]) > 0:
                run = True
            else:
                run = False
            if run == True:
                nnn = splitext(name)
                yex = nnn[1].replace('.','')
                vvv = len(nnn[0].split('/')) - 1
                yn = nnn[0].split('/')[vvv].replace('.','')
                name = f'modules/{yn}/main.{yex}'
                test = isfile(name)
                if test:
                    ex = splitext(name)[1].replace(".","")
                    if ex in self.lang.keys():
                        c = self.lang[ex].replace("$MODULE",name)
                        name = f'$EX${name}'
                        self.modules[name] = c
                    else:
                        print(f'[!] Not supported * {splitext(name)[1]} *')
                        return 0
                else:
                    print(f'[!] |{name}| The file does not exist')
                    return 0
            else:
                name = f'modules.{name}'
                c = importlib.import_module(name.replace('.py',''))
                self.modules[name] = c
            return c
        except Exception as e:
            print(e)
    def exeman(self,cmd,oo):
        oo['domain'] = ur(oo['url']).netloc
        oc = oo.copy()
        oc['ALL'] = oo.copy()
        s = subprocess.call(cmd.format(**oc),shell=True)
        return s
    def run(self,opts,r):
        opt = opts.copy() # copy user options
        with concurrent.futures.ThreadPoolExecutor(max_workers=opts['threads']) as executor:
            mres = []
            for url in opts['urls']:
                opt['url'] = url
                for n,module in self.modules.items():
                    if n.startswith('$EX$'):
                        mres.append(executor.submit(self.exeman,module,opt))
                    elif module.main.__code__.co_argcount >= 2:
                        mres.append(executor.submit(module.main, opt,r))
                    else:
                        mres.append(executor.submit(module.main,opt))
                opt = opts.copy()
            for future in concurrent.futures.as_completed(mres):
                res = future.result()
                if res:
                    res = str(res)
                    print(res.replace(r'$EX$',''))
