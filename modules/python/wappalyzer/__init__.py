from core.libs import Http
from .analyze import Analyze


def main(opts: dict, http: Http):
    result = Analyze(opts, http).start()
    print(result)
