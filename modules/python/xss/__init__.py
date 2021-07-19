from .xss import Scan
from urllib.parse import urlparse as ur
from core.libs import show_error

def main(opts,r):
    scanner = Scan(opts,r)
    # If Query in the URL 
    if ur(opts['url']).query:
        scanner.start(url=opts['url'], methods=opts['methods'])
    show_error('xss', "No query in the URL")