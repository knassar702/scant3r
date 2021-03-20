from . import Reflect


def main(opts,r):
    R = Reflect(r)
    v = R.start(opts['url'],opts['methods'])
    if v:
        for i in v.keys():
            print(f'[Refelct] Found :> {v[i]} {i}')
    return v
