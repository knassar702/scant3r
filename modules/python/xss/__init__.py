from .xss import Xss
from urllib.parse import urlparse as ur
from core.libs import show_error

def main(opts,r):
    # If Query in the URL 
    if ur(opts['url']).query:
        Xss(opts,r).start()
    else: 
        show_error('xss', "No query in the URL")