#!/usr/bin/env python3
__author__ = 'Khaled Nassar'
__email__ = 'knassar702@gmail.com'
__version__ = '0.8#Beta'

import os,sys

# check if python version high up 3.6
if sys.version_info < (3, 6):
    print('[-] Scant3r requires python >= 3.6')
    sys.exit()

import colorama , logging
from core.libs import Args, Http, MLoader, logo, Colors
from urllib.parse import urlparse

colorama.init()
# set the path to scant3r folder
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Load user args
opts = Args().get_args()

# Display Logo
logo()

# Start Module Loader Class
M = MLoader()

# scant3r logger
log = logging.getLogger('scant3r')

# Colors Class
color = Colors()
if __name__ == '__main__':
    
    if len(opts['urls']) <= 0:
        # listen to pipe
        log.debug('listen to pipe input')
        if os.isatty(0):
            log.error('No Targets ')
            exit()
        for url in sys.stdin:
            opts['urls'].append(url.rstrip())
        
    # (-g option) , add famous parameters
    if opts['genparam']:
        log.debug('add parameters for url')
        np = 'q=&searchFor=&query=&Searchfor=goButton=&s=&search=&id=&keyword=&query=&page=&keywords=&url=&view=&cat=&name=&key=&p=&test=&artist=&user=&username=&group='
        for url in opts['urls']:
            url = url.rstrip()
            ind = opts['urls'].index(url)
            
            if len(urlparse(url).query) > 0:
                np = '&{}'.format(np)
            else:
                np = '?{}'.format(np)
                
            opts['urls'][ind] = '{url}{np}'.format(url=url,np=np)
            
    if opts['modules']:
        # load modules
        for module in opts['modules']:
            log.debug(f'Load {color.bwhite}{module}{color.rest} Module')
            M.get(module)

        # start all modules (main function)
        for Module in M.modules.keys():
            log.info(f'Run {color.bwhite}{Module}{color.rest}')
        M.run(opts, Http(opts))
