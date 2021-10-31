from .code import Cve
from core.libs import Http

def main(opts: dict, http: Http):
    Cve(opts,http).start()
