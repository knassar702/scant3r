from .ssti import Ssti
from core.libs import alert_bug, Http

def main(opts: dict, http: Http):
    v = Ssti(opts, http).start()
    if v:
        alert_bug('SSTI',**v)
