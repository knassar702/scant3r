from .finder import Scan
from core.libs import alert_bug

def main(opts, r, api=False):
    result = Scan(opts, r).scan()
    if result:
        for i,c in result.items():
            alert_bug('FINDER',**c)
        if api:
            return result
