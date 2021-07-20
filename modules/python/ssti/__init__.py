from .ssti import Ssti
from core.libs import alert_bug

def main(opts,r):
    v = Ssti(opts,r).start()
    if v:
        alert_bug('SSTI',**v)
