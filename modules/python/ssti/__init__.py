from .ssti import Ssti
from core.libs import alert_bug

def main(opts, http):
    v = Ssti(opts, http).start()
    if v:
        alert_bug('SSTI',**v)
