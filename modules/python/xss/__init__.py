from .xss import Xss
from urllib.parse import urlparse as ur
from core.libs import show_error, Http
from logging import getLogger

log = getLogger('scant3r')

def main(opts: dict, http: Http):
    # If Query in the URL 
    if ur(opts['url']).query:
        Xss(opts, http).start()
    else: 
        log.debug('XSS_PARAMS: NO URL QUERY')
