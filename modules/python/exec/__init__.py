from .exec import Exec
from core.libs import Http

def main(opts: dict, http: Http):
    Exec(opts,http).start()
