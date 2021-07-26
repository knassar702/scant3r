from .xss_param import XssParam
from urllib.parse import urlparse as ur
from core.libs import show_error, Http
from logging import getLogger

log = getLogger('scant3r')

def main(opts: dict, http: Http):
    # If Query in the URL 
    if ur(opts['url']).query:
        XssParam(opts, http).start()
    else:
        log.debug('XSS_PARAMS: NO URL QUERY')
