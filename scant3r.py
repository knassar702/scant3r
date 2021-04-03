#!/usr/bin/env python3
__author__ = 'Khaled Nassar'
__email__ = 'knassar702@gmail.com'
__version__ = '0.7#Beta'

import os,sys

# check if python version high up 3.6
if sys.version_info < (3, 6):
    print('[-] Scant3r requires python >= 3.6')
    sys.exit()
import colorama
from core.libs import Args,http,logo,Colors,MLoader
from core.api import Server
from urllib.parse import urlparse,urljoin

colorama.init()
# set the path of scant3r folder
os.chdir(os.path.dirname(os.path.abspath(__file__)))


# Load user args
a = Args()
opts = a.start()
if opts['nologo']:
    pass
else:
    logo()
# ---
# Configure http options (proxy,headers etc..)
msg = http(opts)
# Start Module Loader Class
M = MLoader()
s = Server(msg,opts)

if __name__ == '__main__':
    if opts['api']:
        app = Server(msg,opts)
        app.run()
    if len(opts['urls']) <= 0:
        # get urls from pipe
        for url in sys.stdin:
            opts['urls'].append(url.rstrip())
    # (-g option) , add famouse parameters
    if opts['genparam']:
            for url in opts['urls']:
                url = url.rstrip()
                ind = opts['urls'].index(url)
                if len(urlparse(url).query) == 0:
                    opts['urls'][ind] = urljoin(url,'?q=&searchFor=&query=&Searchfor=goButton=&s=&search=&id=&keyword=&query=&page=&keywords=&url=&view=&cat=&name=&key=&p=&test=&artist=&user=&username=&group=')
    if opts['modules']:
        # load modules
        for MM in opts['modules']:
            M.get(MM)
        # start all modules (main function)
        M.run(opts,msg)
