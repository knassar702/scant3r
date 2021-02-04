#!/usr/bin/env python3
from optparse import OptionParser
from .colors import *
from .logo import *
from .data import *
import sys



def load_opts():
        helper = r"""{yellow}
Options:
    -h  | show help message and exit
    -n  | remove scant3r banner
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
    -d  | Debugging Mode (show req/resp)
    -S  | use scant3r scanner after use modules
Pipe:
    $ echo "http://web.com/?v=1" | scant3r
List:
    $ scant3r -l web.txt

Wiki:
    ScanT3r Modules
    - https://github.com/knassar702/scant3r/wiki/ScanT3r-Modules

    how to wirte your own scant3r script
    - https://github.com/knassar702/scant3r/wiki/writing-your-own-scant3r-module
    
    ScanT3r API
    - https://github.com/knassar702/scant3r/wiki/ScanT3r-API

    Usage
    - https://github.com/knassar702/scant3r/wiki/Usage

Examples:

    # simple scan
        $ echo 'http://php.net' | ./scant3r.py -w 100 -R
    # Find SSRF Parameters
        $ echo 'http://testphp.vulnweb.com/showimage.php' | ./scant3r.py -m lorsrf -w 100 -R -x http://myhost
    # Find Files
        $ cat subdomains.txt | ./scant3r.py -m paths -w 100 -R
    # scan headers from custom payloads
        $ cat subdomains.txt | ./scant3r.py -m headers -w 100 -R
    # get live http/s
        $ cat subdomains.txt | ./scant3r.py -m httper -w 100 -R
    # get live hosts
        $ cat subdomains.txt | ./scant3r.py -m hostping -w 100
    # find host header injection
        $ cat subdomains.txt | ./scant3r.py -m hostinj -w 100 -R


{rest}
""".format(yellow=yellow,rest=rest)
        optp = OptionParser(add_help_option=False)
        optp.add_option("-h",'--help',dest='help',action='store_true')
        optp.add_option('-c',dest='cookie')
        optp.add_option('-r',dest='redirect',action='store_true')
        optp.add_option('-p',dest='proxy')
        optp.add_option('-n','--nologo',dest='nologo',action='store_true')
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
        if opts.help:
            logo()
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
        urls = []
        if opts.List:
            List = opts.List
            try:
                List = open(List,'r')
                for url in List:
                    urls.append(url.rstrip())
            except Exception as e:
                print(e)
                sys.exit()
        else:
            List = None
            for pipe_url in sys.stdin:
                pipe_url = pipe_url.rstrip()
                urls.append(pipe_url)
        all_options = {
    'proxy':proxy,
    'cookie':cookie,
    'timeout':timeout,
    'Headers':Header,
    'list':opts.List,
    'random-agent':Random,
    'threads':thr,
    'module':module,
    'url':urls,
    'use_scanner':opts.use_scanner,
    'host':host,
    'debug':opts.dump,
    'redirect':opts.redirect,
    'List':opts.List,
    'API':opts.api,
    'nologo':opts.nologo,
    'help':opts.help,
            }
        return all_options
