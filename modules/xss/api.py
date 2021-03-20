from .xss import Scan



def main(opts,r):
    scanner = Scan(opts,r)
    return scanner.start(url=opts['url'],methods=opts['methods'])
