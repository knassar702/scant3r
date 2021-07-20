from core.libs import alert_bug
from .rce import Scan

def main(opts,r):
    v = Scan(opts, r).scan()
    if v:
        alert_bug('Remote Code Execution',**v)
