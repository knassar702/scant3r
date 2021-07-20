from .sqli import Sqli
from urllib.parse import urlparse

def main(opts,http):
    if urlparse(opts['url']).query:
        return Sqli(opts,http).start()
