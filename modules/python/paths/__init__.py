from .paths import Paths
from core.libs import Http

def main(opts: dict, http: Http):
    Paths(opts, http).start()
