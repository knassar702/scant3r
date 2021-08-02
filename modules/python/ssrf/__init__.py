from .ssrf import Ssrf
from core.libs import Http

def main(opts: dict, http: Http):
    return Ssrf(opts, http).start()
    
