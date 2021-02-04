#!/usr/bin/env python3
__name__ = 'ScanT3r'
__author__ = 'Khaled Nassar'
__email__ = 'knassar702@gmail.com'
__version__ = '0.6#Beta'

from .colors import *
class ShowMessage:
    def __init__():
        pass
    def error(msg):
        print(f'''
[{red}-{red}] {msg}
        ''')
    def bug(bug=None,payload=None,method=None,parameter=None,link=None,target=None):
        if method.upper() == 'GET':
            print(f'''
[{red}!{rest}] Bug : {bug}
[{red}!{rest}] Payload: {payload}
[{red}!{rest}] Method: {method}
[{red}!{rest}] parameter: {parameter}
[{red}!{rest}] Link: {link}
|-----------------|
        ''')
        else:
            print(f'''
[{red}!{rest}] Bug : {bug}
[{red}!{rest}] Payload: {payload}
[{red}!{rest}] Method: {method}
[{red}!{rest}] parameter: {parameter}
[{red}!{rest}] Data: {link}
[{red}!{rest}] Target: {target}
|-----------------|
        ''')
    def bug_Header(bug=None,payload=None,method=None,header=None,target=None):
        print(f'''
[{red}!{rest}] Bug : {bug}
[{red}!{rest}] Header: {header}
[{red}!{rest}] Payload: {payload}
[{red}!{rest}] Method: {method}
[{red}!{rest}] URL: {target}
|-----------------|
        ''')
