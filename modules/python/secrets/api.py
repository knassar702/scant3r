from .secrets import Secrets
from core.libs import Http

def main(opts: dict, http: Http):
    return Secrets(opts, Http).start()
