from .rce import Rce
from core.libs import alert_bug, Http

def main(opts: dict, http : Http):
    dict_result = Rce(opts, http).start()
    if dict_result:
        return alert_bug('Remote Code Execution',**dict_result)
