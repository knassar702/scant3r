from reflect import Reflect
from core.libs import Http

def main(opts: dict, http : Http):
    list_result = Reflect(opts, http).start()
    if list_result:
        for i in list_result.keys():
            print(f'[Refelct] Found :> {list_result[i]} {i}')
    return list_result
