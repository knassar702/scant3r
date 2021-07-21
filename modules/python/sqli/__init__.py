from .sqli import Sqli
from core.libs import Http

def main(opts: dict, http: Http):
    c = Sqli(opts, http).start()
    # C is always an empty dict
    if c:
        return c 