from .xss import Scan



def main(opts,r):
    scanner = Scan(opts,r)
    return scanner.start(opts['url'],methods=opts['methods'])
