from .xss_param import XssParam
from core.libs import Http 

def main(opts: dict, http : Http):
    return XssParam(opts,http).start()
