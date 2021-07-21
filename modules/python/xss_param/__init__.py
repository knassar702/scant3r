from .xss_param import XssParam
from urllib.parse import urlparse as ur
from core.libs import show_error, Http

def main(opts: dict, http: Http):
    # If Query in the URL 
    if ur(opts['url']).query:
        XssParam(opts, http).start()
    else: 
        show_error('xss_param', "No query in the URL")
    