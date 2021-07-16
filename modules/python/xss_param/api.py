from .xss import Scan



def main(opts,r):
    c = Scan(opts,r)
    return c.start(opts['methods'])
