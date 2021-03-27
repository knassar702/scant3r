from .xss import Scan
from urllib.parse import urlparse

def main(opts,http):
    scanner = Scan(opts,r)
    if urlparse(opts['url']).query:
        return scanner.start(url=opts['url'],opts['methods'])
