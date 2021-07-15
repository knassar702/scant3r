#!/usr/bin/env python3

__author__ = 'Khaled Nassar'
__email__ = 'knassar702@gmail.com'
__version__ = '0.7#Beta'

import importlib
import concurrent.futures
import yaml
from urllib.parse import urlparse as ur
from os.path import splitext, isfile
import subprocess

class MLoader:
    def __init__(self):
        self.thr = list()
        self.modules = dict()
        self.scripts = dict()
        
    def get(self, name: str, ourlist: bool = True):
        try:
            c = None
            ih = isfile(f'modules/{name}/run.yaml')
            cki = isfile(f'modules/{name}/__init__.py')
            
            # if Not __init__.py and run.yaml present 
            # Execution No Python Script
            if cki == False and ih == True:
                ff = yaml.safe_load(open(f'modules/{name}/run.yaml','r'))
                name = f'$EX${name}'
                if ourlist:
                    self.scripts[name] = ff['exec']

            # If file __init__.py in modules
            if cki == True:
                name = f'modules.{name}'
                # Import the modules and remove .py if need                
                c = importlib.import_module(name.replace('.py',''))
                if ourlist:
                    # Add module to the dict
                    self.modules[name] = c
            return c
        except Exception as e:
            print(e)
            
    def exeman(self, name, cmd, oo):
        ff = yaml.safe_load(open(f'modules/{name}/run.yaml','r'))
        oo['domain'] = ur(oo['url']).netloc
        oc = oo.copy()
        oc['ALL'] = oo.copy()
        acmd = cmd.format(**oc).replace(r'$SCPATH',f'modules/{name}')
        s = subprocess.Popen([acmd],shell=True, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        sres,_err = s.communicate()
        resu = f'\n[MODULE-{name.upper()}] {acmd}\n[OUTPUT]: [\n\n{sres}\n]\n-------\n'
        if 'pass' in ff.keys():
            module_name = ff['pass']['module']
            change_option = ff['pass']['option']
        if len(sres) > 0:
            return resu
        return 
    
    def run(self, opts : dict, r):
        # Start threading
        with concurrent.futures.ThreadPoolExecutor(max_workers=opts['threads']) as executor:
            mres = list()
            
            for url in opts['urls']:
                # copy user options
                opt = opts.copy() 
                opt['url'] = url
                
                # Execution of scripts 
                for n,module in self.scripts.items():
                    mres.append(executor.submit(self.exeman,n.replace('$EX$','').replace('/','.'),module,opt))
                
                # Execution of modules     
                for n,module in self.modules.items():
                    # Check the number of argument needed by the module                     
                    if module.main.__code__.co_argcount >= 2:
                        mres.append(executor.submit(module.main, opt, r))
                    else:
                        mres.append(executor.submit(module.main, opt))
            
            # When the scan is completed
            for future in concurrent.futures.as_completed(mres):
                res = future.result()
                if res:
                    res = str(res)
                    print(res.replace(r'$EX$',''))
