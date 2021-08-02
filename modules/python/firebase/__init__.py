from .firebase import Firebase
from core.libs import Http

def main(opts: dict, http: Http):
    Firebase(opts,http).start()
