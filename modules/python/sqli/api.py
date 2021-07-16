from . import start
from urllib.parse import urlparse


def main(opts,http):
    scanner = start(opts,http)
    if urlparse(opts['url']).query:
        return scanner
