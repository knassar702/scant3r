#!/usr/bin/env python3

__author__ = 'Khaled Nassar'
__email__ = 'knassar702@gmail.com'
__version__ = '0.7#Beta'

import importlib
import concurrent.futures
import yaml
from urllib.parse import urlparse as ur
from os.path import isfile
from glob import glob
import subprocess, logging
from core.libs import Http

log = logging.getLogger('scant3r')

class MLoader:
    def __init__(self):
        self.thr = list()
        self.modules = dict()
        self.scripts = dict()

    def get(self, name: str, ourlist: bool = True):
        try:
            c = None
            for our_file in glob(f'modules/*/{name}'):
                if type(our_file) is list:
                    # remove duplicates module name
                    our_file = our_file[0]

                ih = isfile(f'{our_file}/run.yaml')
                cki = isfile(f'{our_file}/__init__.py')
                
                # if Not __init__.py and run.yaml present 
                # Execution No Python Script
                if not cki and ih:
                    ff = yaml.safe_load(open(f'{our_file}/run.yaml','r'))
                    name = f'$EX${name}'
                    if ourlist:
                        self.scripts[name] = ff['exec']
                        
                # If file __init__.py in modules
                if cki:
                    name = f'modules.python.{name}'
                    # Import the modules
                    c = importlib.import_module(name)
                    if ourlist:
                        # Add module to the dict
                        self.modules[name] = c
                return c
        except Exception as e:
            print(e)
            
    def exeman(self, name, cmd, oo):
        module_folder = glob(f'modules/*/{name}/run.yaml')
        if type(module_folder) is list:
            module_folder = module_folder[0]
        ff = yaml.safe_load(open(module_folder,'r'))
        oo['domain'] = ur(oo['url']).netloc
        oc = oo.copy()
        oc['ALL'] = oo.copy()
        acmd = cmd.format(**oc).replace(r'$SCPATH',f'modules/{module_folder.split("/")[1]}/{name}')
        s = subprocess.Popen([acmd],shell=True, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        sres,_err = s.communicate()
        resu = f'\n[MODULE-{name.upper()}] {acmd}\n[OUTPUT]: [\n\n{sres}\n]\n-------\n'
        if 'pass' in ff.keys():
            module_name = ff['pass']['module']
            change_option = ff['pass']['option']
        if len(sres) > 0:
            return resu
        return 
    
    def run(self, opts: dict, http: Http):
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
                    mres.append(executor.submit(module.main, opt, http))
            
            # When the scan is completed
            for future in concurrent.futures.as_completed(mres):
                res = future.result()
                if res:
                    res = str(res)
                    print(res.replace(r'$EX$',''))
