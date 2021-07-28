#!/usr/bin/env python3
import argparse , logging, yaml
from .data import *
from .log import CustomFormatter
from .colors import Colors
from .logo import logo


log = logging.getLogger('scant3r')

class Args:
    def __init__(self):
        try:
            log.debug('load opts & help config files')
            self.conf = yaml.safe_load(open('conf/opts.yaml','r'))
            self.help = open('conf/help.txt','r')
        except Exception as e:
            log.error(e)
            exit()
    
    # Add an argument to a parser 
    def set_argument(self, options: list, name: str, parser: argparse.ArgumentParser):
        dict_option = {}
        dict_option['name'] = str(name)
        for option in options: 
            if 'option' in option.keys():
                dict_option['small'] = option['option'][0]
                dict_option['large'] = option['option'][1]
                
            if 'type' in option.keys():
                dict_option['type'] = str
                if option['type'] == 'int':
                    dict_option['type'] = int 
                if option['type'] == 'boolean':
                    dict_option['type'] = bool

            if 'save_content' in option.keys():
                dict_option['action'] = "store_true"
                if option['save_content'] == True:   
                    dict_option['action'] = "store"
                    
            if 'help' in option.keys():
                dict_option['help'] = option['help']
            if 'default' in option.keys():
                dict_option['default'] = option['default']
                if option['default'] == "{}":
                    dict_option['default'] = {}
                if option["default"] == "[]":
                    dict_option['default'] = []
            if 'default_action' in option.keys():
                try:
                    # execute command for default value :D
                    dict_option['default'] = eval(option['default_action'])
                except Exception as e:
                    log.error(e)
        if dict_option['type'] != bool: 
            parser.add_argument(dict_option['small'], dict_option['large'], 
                        dest=dict_option['name'], type=dict_option['type'], 
                        default=dict_option['default'], action=dict_option['action'], 
                        help=dict_option['help'])
        else: 
            parser.add_argument(dict_option['small'], dict_option['large'], 
                                dest=dict_option['name'], default=dict_option['default'], 
                                action=dict_option['action'], help=dict_option['help'])
    
    # Create the dict with args
    def create_dict_args(self, args : argparse.Namespace) -> dict:
        dict_args = { "urls" : [] }
        args = vars(args)
        for name, value in args.items(): 
            if value == 0 or value == [] or value == {} or value == False:
                dict_args[name] = value
            else : 
                dict_exe = list(filter(lambda item : 'exec' in item.keys(), self.conf[name]))[0]
                if dict_exe:
                    exec(dict_exe['exec'])
        return dict_args
    
    # Take text from help.txt and transfrom to str
    def epilog_text(self) -> str: 
        text = ''
        for txt in self.help:
            txt = txt.replace(r'\t','\t').replace(r'\n','\n')
            text += txt
        return text
     
    # Return args in dict 
    def get_args(self) -> dict:
        parser = argparse.ArgumentParser(epilog=self.epilog_text(), formatter_class=argparse.RawTextHelpFormatter)
        for name,options in self.conf.items():
            self.set_argument(options, name, parser)
        args = parser.parse_args()    
        return self.create_dict_args(args)

