from .xss import Scan



def main(opts,r):
    c = Scan(opts,r)
    c.start(opts['methods'])
