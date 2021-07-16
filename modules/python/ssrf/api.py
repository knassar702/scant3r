from .ssrf import start

def main(opts,r):
    return start(opts,opts['url'],r,opts['methods'])
