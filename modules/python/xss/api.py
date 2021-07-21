from .xss import Xss
from urllib.parse import urlparse
from core.libs import Http

def main(opts: dict, http: Http):
    if urlparse(opts['url']).query:
        return Xss(opts,http).start()
    return
