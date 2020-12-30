#!/usr/bin/env python3
#__name__ = 'ScanT3r'
__author__ = 'Khaled Nassar'
__email__ = 'knassar702@gmail.com'
__version__ = '0.6#Beta'
import sys
if sys.version_info < (3, 6):
    print('[-] Scant3r requires python >= 3.6')
    sys.exit()
from optparse import OptionParser
from libs import NewRequest as nq
from libs import extractHeaders,post_data,dump_alloptions
from modules import *
from threading import Thread
from queue import Queue
from core import ShowMessage as show
from core import *
from wordlists import XP
a = Queue()
b = Queue()
c = Queue()
d = Queue()
r = Queue()
helper = """{yellow}
Options:
    -h  | show help message and exit
    -c  | add cookies
    -r  | follow redirects
    -p  | add (http/s) proxy
    -t  | Second of timeout (default 10)
    -w  | Number of worker (default 20)
    -l  | add targets list
    -H  | add custom header (ex:-H='HM: True\nTest: New')
    -m  | run scant3r module (ex: -m=example)
    -R  | random User-agent
    -x  | your host(xsshunter,burp collaborator)
    -d  | Debugging Mode
Pipe:
    $ echo "http://web.com/?v=1" | scant3r
List:
    $ scant3r -l web.txt
{rest}
""".format(yellow=yellow,rest=rest)
optp = OptionParser(add_help_option=False)
optp.add_option("-h",'--help',dest='help',action='store_true')
optp.add_option('-c',dest='cookie')
optp.add_option('-r',dest='redirect',action='store_true')
optp.add_option('-p',dest='proxy')
optp.add_option('--nologo',dest='nologo',action='store_true')
optp.add_option('--api',dest='api',action='store_true')
optp.add_option('-l',dest='List')
optp.add_option('-m',dest='module',action='append')
optp.add_option('-g',dest='gasker')
optp.add_option('-d',dest='dump',action='store_true')
optp.add_option('-S',dest='use_scanner',action='store_true')
optp.add_option('-t',dest='timeout',type='int')
optp.add_option('-w',dest='thr',type='int')
optp.add_option('-H',dest='Header')
optp.add_option('-x',dest='host')
optp.add_option('-R',dest='Random',action='store_true')
opts, args = optp.parse_args()
if opts.nologo:
    pass
else:
    logo()
if opts.help:
    print(helper)
    sys.exit()
if opts.api:
    api = True
else:
    api = False
if opts.host:
    host = opts.host
else:
    host = None
if opts.module:
    module = opts.module
else:
    module = None
if opts.dump:
    dump = opts.dump
else:
    dump = None
if opts.use_scanner:
    use_scanner = True
else:
    use_scanner = False
if opts.thr:
    thr = opts.thr
else:
    thr = 20
if opts.timeout:
    timeout = opts.timeout
else:
    timeout = 10
if opts.Header:
    try:
        Header = extractHeaders(opts.Header)
    except Exception as e:
        print(e)
        sys.exit()
else:
    Header = {}
if opts.Random:
    Random = True
else:
    Random = False
if opts.proxy:
    proxy = opts.proxy
    proxy = {
    'http':proxy,
    'https':proxy
            }
else:
    proxy = None
if opts.cookie:
    cookie = post_data(opts.cookie)
    if cookie == 0:
        print('\n{bad} invalid data'.format(bad=bad))
        sys.exit()
else:
    cookie = None
if opts.redirect:
    redirect = True
else:
    redirect = False
if opts.List:
    List = opts.List
    try:
        List = open(List,'r')
    except Exception as e:
        print(e)
        sys.exit()
else:
    List = None
all_options = {
    'proxy':proxy,
    'cookie':cookie,
    'timeout':timeout,
    'Headers':Header,
    'list':List,
    'random-agent':Random,
    'threads':thr,
    'module':module,
    'url':[],
    'host':host
        }
nq.Setup(proxies=proxy,cookie=cookie,dump=dump,timeout=timeout,random_agents=Random,header=Header,redirect=redirect)
XP.Setup(host=host)
if __name__ == '__main__':
    if api:
        from api import app
        app.run(host='0.0.0.0',threaded=True,port=6040)
    if List:
        for url in List:
            all_options['url'].append(url)
    else:
        for url in sys.stdin:
            url = url.rstrip()
            all_options['url'].append(url)
    if opts.nologo:
        pass
    else:
        dump_alloptions(all_options)
    from vuln import txss,tcrlf,trce,tsqli,tssti
    if module:
        for M in module:
            Import.Get(M)
            Import.run(all_options)
        if use_scanner:
            pass
        else:
            sys.exit()
    for i in range(thr):
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
    for url in all_options['url']:
        url = url.rstrip()
        if '?' in url and '=' in url:
            pass
        else:
            url += '?q=&s=&search=&id=&keyword=&query=&page=&keywords=&url=&view=&cat=&name=&key=&p=&test=&artist&user=&username=&group='
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

