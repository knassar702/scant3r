#!/usr/bin/env python3
__author__ = 'Khaled Nassar'
__email__ = 'knassar702@gmail.com'
__version__ = '0.8#Beta'

import os,sys

# check if python version high up 3.6
if sys.version_info < (3, 6):
    print('[-] Scant3r requires python >= 3.6')
    sys.exit()
    
import colorama
from core.libs import Args, Http, Colors, MLoader, logo
from core.api import Server
from urllib.parse import urlparse, urljoin

colorama.init()
# set the path to scant3r folder
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Load user args
opts = Args().get_args()

# Display Logo
if opts['nologo'] == False:
    logo()

# Start Module Loader Class
M = MLoader()

if __name__ == '__main__':
    # launch scant3r api server
    if opts['api']:
        app = Server(opts)
        app.run()
        sys.exit()
    
    if len(opts['urls']) <= 0:
        # listen to pipe
        for url in sys.stdin:
            opts['urls'].append(url.rstrip())
        
    # (-g option) , add famous parameters
    if opts['genparam']:
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
            M.get(module)
    
        # start all modules (main function)
        M.run(opts, Http(opts))
