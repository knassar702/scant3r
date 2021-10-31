#!/usr/bin/env python3

__author__ = 'Khaled Nassar'
__email__ = 'knassar702@gmail.com'
__version__ = '0.7#Beta'

import importlib , re , concurrent.futures , yaml , subprocess, logging
from urllib.parse import urlparse
from os.path import isfile
from glob import glob
from core.libs import Http , alert_bug,alert_script ,show_error

log = logging.getLogger('scant3r')


class MLoader:
    def __init__(self):
        self.thr: list = list()
        self.modules: dict = dict()
        self.scripts: dict = dict()

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
            log.error(e)
    def exeman(self, name: str, cmd: str, opts: dict) -> str:
        try:
            # find run.yaml file
            module_folder = f'modules/scripts/{name}/run.yaml'
            # load run.yaml config file
            file_config = yaml.safe_load(open(module_folder,'r'))
            opts['domain'] = urlparse(opts['url']).netloc
            new_opts = opts.copy()
            new_opts['ALL'] = opts.copy()
            acmd = cmd.format(**new_opts).replace(r'$SCPATH',f'modules/scripts/{name}')
            # Execute the command
            exec_cmd = subprocess.Popen([acmd],shell=True, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            script_results , err = exec_cmd.communicate() # Get the output of the command
            if len(script_results) > 0:
                if 'remove' in file_config.keys():
                    if file_config['remove']['regex']:
                        # remove custom text from scripts output (eg: logo,logging)
                        script_results = re.sub(file_config['remove']['word'],script_results)
                    else:
                        script_results = script_results.lstrip(file_config['remove']['word'])
                if 'stop_matching' in file_config.items():
                    pass
                else: 
                    # matching for script results
                    script_results = re.findall(file_config['match'],script_results)
                    if len(script_results):
                        script_results = "\n".join(script_results)
                        alert_script(name=name,command=acmd,results='\n\n'+err+'\n\n'+script_results) # Display scirpt output
        except Exception as e:
            log.debug(e)
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
                for name, script in self.scripts.items():
                    mres.append(executor.submit(self.exeman, name.replace('$EX$','').replace('/','.'), script, opt))
                
                # Execution of modules     
                for _, module in self.modules.items():
                    mres.append(executor.submit(module.main, opt, http))
            
#            # When the scan is completed
            for future in concurrent.futures.as_completed(mres):
                res = future.result()
                if res:
                    print(res)
#                    if res[0] == 'alert':
#                        self.msg.Alert(res[1])
#                    else:
#                        self.msg.Error(res[1])
