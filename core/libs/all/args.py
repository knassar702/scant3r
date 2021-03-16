#!/usr/bin/env python3

from optparse import OptionParser
from .colors import rest,yellow
from .data import *
import yaml

class Args:
    def __init__(self):
        try:
            self.conf = yaml.safe_load(open('core/settings/opts.yaml','r'))
        except Exception as e:
            print(f"[Args] {e}")
            exit()
        ho = ''
        self.urls = []
        for name,option in self.conf.items():
            vv = []
            for _ in option:
                if 'help' in _.keys():
                    vv.append(_["help"])
                if 'option' in _.keys():
                    vv.append(_['option'])
                if len(vv) == 2:
                    ho += f'  {vv[0]} | {vv[1]}\n'
                    vv.clear()
                    break
        self.help = r"""{yellow}
Options:
  -h | show help menu and exit
{ho}
Pipe:
    $ echo "http://web.com/?v=1" | scant3r
List:
    $ scant3r -l web.txt
Wiki:
    how to wirte your own scant3r script
    - https://github.com/knassar702/scant3r/wiki/writing-your-own-scant3r-module 
    ScanT3r API
    - https://github.com/knassar702/scant3r/wiki/ScanT3r-API
    Usage
    - https://github.com/knassar702/scant3r/wiki/Usage
    Write API Module
    - https://github.com/knassar702/scant3r/wiki/write-module-for-api
Examples:
    # simple scan
        $ echo 'http://testphp.vulnweb.com/search.php?test=query&searchFor=test&goButton=go' | ./scant3r.py -w 100 -R
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
    # Run Multi modules
        $ ./scant3r.py -l subdomains.txt -m example -m example -m example -w 100 -R
{rest}
""".format(ho=ho,yellow=rest,rest=yellow)
    def start(self):
        optp = OptionParser(add_help_option=False)
        optp.add_option("-h",'--help',dest='help',action='store_true')
        for name,value in self.conf.items():
            op = {'name':name}
            for _ in value:
                for o,v in _.items():
                    op[o] = v
            if op['default'] == '[]':
                op['default'] = []
            elif op['default'] == '{}':
                op['default'] = {}
            if op['type']:
                optp.add_option(op['option'],default=op['default'],type=op['type'],action=op['action'],dest=op['name'])
            else:
                optp.add_option(op['option'],default=op['default'],action=op['action'],dest=op['name'])
        opts, args = optp.parse_args()
        if opts.help:
            print(self.help)
            exit()
        for name,value in self.conf.items():
            op = {'name':name}
            for _ in value:
                for o,v in _.items():
                    op[o] = v
            if eval(f'opts.{name}'):
                exec(op['exec'])
            else:
                exec(f'self.{name} = {op["default"]}')
        c = vars(self)
        del c['conf']
        del c['help']
        return c
