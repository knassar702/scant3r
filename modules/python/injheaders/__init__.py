from .injheaders import Injheaders 
from core.libs import Http

def main(opts: dict, http: Http):
    Injheaders(opts, http).start()
