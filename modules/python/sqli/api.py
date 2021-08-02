from .sqli import Sqli
from urllib.parse import urlparse
from core.libs import Http

def main(opts: dict, http: Http):
    if urlparse(opts['url']).query:
        return Sqli(opts,http).start()
