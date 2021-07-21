from .xss import Xss
from urllib.parse import urlparse as ur
from core.libs import show_error, Http

def main(opts: dict, http: Http):
    # If Query in the URL 
    if ur(opts['url']).query:
        Xss(opts, http).start()
    else: 
        show_error('xss', "No query in the URL")