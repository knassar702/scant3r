from .rce import Rce
from core.libs import alert_bug

def main(opts,r):
    dict_result = Rce(opts, r).start()
    if dict_result:
        alert_bug('Remote Code Execution',**dict_result)
