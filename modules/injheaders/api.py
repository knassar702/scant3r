from . import Scan

def main(opts,r):
    s = Scan(opts,r)
    return s.start(url=opts['url'],methods=opts['methods'])
