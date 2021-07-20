from .finder import Scan
from core.libs import alert_bug

def main(opts, http, api=False):
    result = Scan(opts, http).scan()
    if result:
        for i,c in result.items():
            alert_bug('FINDER',**c)
        if api:
            return result
