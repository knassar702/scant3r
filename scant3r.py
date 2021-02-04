#!/usr/bin/env python3
__author__ = 'Khaled Nassar'
__email__ = 'knassar702@gmail.com'
__version__ = '0.7#Beta'

"""
   _____           _   _ _   ____       
  / ____|         | \ | | | |___ \      
 | (___   ___ __ _|  \| | |_  __) |_ __ 
  \___ \ / __/ _` | . ` | __||__ <| '__|
  ____) | (_| (_| | |\  | |_ ___) | |   
 |_____/ \___\__,_|_| \_|\__|____/|_|   
                                        
	# by: Khaled Nassar @knassar702
	# Link: github.com/knassar702/scant3r                                        
"""
import sys,colorama
if sys.version_info < (3, 6):
    print('[-] Scant3r requires python >= 3.6')
    sys.exit()
colorama.init()


from libs import NewRequest as nq
from modules import *
from threading import Thread
from queue import Queue
from libs import ShowMessage as show
from libs import *
from wordlists import XP

a = Queue()
b = Queue()
c = Queue()
d = Queue()
r = Queue()

all_opts = load_opts()
if all_opts['nologo']:
    pass
else:
    logo()
nq.Setup(proxies=all_opts['proxy'],cookie=all_opts['cookie'],dump=all_opts['debug'],timeout=all_opts['timeout'],random_agents=all_opts['random-agent'],header=all_opts['Headers'],redirect=all_opts['redirect'])
XP.Setup(host=all_opts['host'])

if __name__ == '__main__':
    if all_opts['API']:
        from api import app
        app.run(host='0.0.0.0',threaded=True,port=6040)
    if all_opts['nologo']:
        pass
    else:
        dump_alloptions(all_opts)
    from vuln import txss,tcrlf,trce,tsqli,tssti
    if all_opts['module']:
        for M in all_opts['module']:
            myfunc = Get(M)
            Import.run(myfunc)
        if all_opts['use_scanner']:
            pass
        else:
            sys.exit()
    for i in range(all_opts['threads']):
        p1 = Thread(target=txss,args=(a,))
        p1.daemon = True
        p1.start()
        p2 = Thread(target=tsqli,args=(b,))
        p2.daemon = True
        p2.start()
        p3 = Thread(target=trce,args=(c,))
        p3.daemon = True
        p3.start()
        p4 = Thread(target=tssti,args=(d,))
        p4.daemon = True
        p4.start()
        p5 = Thread(target=tcrlf,args=(r,))
        p5.daemon = True
        p5.start()
    for url in all_opts['url']:
        url = url.rstrip()
        if '?' in url and '=' in url:
            pass
        else:
            url += '?q=&u=&s=&search=&id=&keyword=&query=&page=&keywords=&url=&view=&cat=&name=&key=&p=&test=&artist=&user=&username=&group='
        a.put(url)
        b.put(url)
        c.put(url)
        d.put(url)
        r.put(url)
    a.join()
    b.join()
    c.join()
    d.join()
    r.join()

