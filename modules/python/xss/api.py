from .xss import Xss
from urllib.parse import urlparse

def main(opts,http):
    if urlparse(opts['url']).query:
        return Xss(opts,http).start()
    return
