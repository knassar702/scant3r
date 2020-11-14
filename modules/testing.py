#!/usr/bin/env python3

import os
import requests

def data():
    return {
    'use_scanner':False,
    'options':[
        'cookie',
        'proxy',
        'url',
        'timeout',
        'Headers'
        ]
            }

url = 'http://google.com'
def run(option):
    #r = requests.get(url)
    for url in option['url']:
        print(url)
