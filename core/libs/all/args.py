#!/usr/bin/env python3

from optparse import OptionParser
from .data import *
from .colors import Colors
from .logo import logo
import yaml

class Args:
    def __init__(self):
        try:
            self.conf = yaml.safe_load(open('core/settings/opts.yaml','r'))
            self.moretxt = ''
            self.hhelp = yaml.safe_load(open('core/settings/help.yaml','r'))
            for v,i in self.hhelp.items():
                i = i.replace(r'\t','\t').replace(r'\n','\n')
                self.moretxt += f'\n{v}:{i}'
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
{moretxt}
{rest}
""".format(
        ho=ho,
        moretxt=self.moretxt,
        yellow=Colors.yellow,
        rest=Colors.rest
        )
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
            logo()
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
