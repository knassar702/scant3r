from .finder import Finder
from core.libs import alert_bug

def main(opts, http, api=False):
    result = Finder(opts, http).start()
    if result:
        for i,c in result.items():
            alert_bug('FINDER',**c)
        if api:
            return result
