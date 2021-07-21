from .sqli import Sqli
from core.libs import Http

def main(opts: dict, http: Http):
    Sqli(opts, http).start()
