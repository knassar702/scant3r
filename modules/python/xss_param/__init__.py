from .xss import Scan
from urllib.parse import urlparse as ur


def main(opts,r):
    c = Scan(opts,r)
    if ur(opts['url']).query:
        c.start(opts['methods'])
