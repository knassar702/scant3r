from . import scan
from core.libs import alert_bug

def main(opts,r):
    s = scan(r,opts['url'],opts['methods'])
    if s:
        return alert_bug('Remote Code Execution',**s)
