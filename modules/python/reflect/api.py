from reflect import Reflect

def main(opts,r):
    list_result = Reflect(opts, r).start
    if list_result:
        for i in list_result.keys():
            print(f'[Refelct] Found :> {list_result[i]} {i}')
    return list_result
