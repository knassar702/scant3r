from .ssti import Scan
from core.libs import alert_bug

def main(opts,r):
    s = Scan(opts,r)
    v = s.scan(opts['url'],methods=opts['methods'])
    if v:
        alert_bug('SSTI',**v)
