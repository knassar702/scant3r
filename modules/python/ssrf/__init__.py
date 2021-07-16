from .ssrf import start

def main(opts,r):
    start(opts,opts['url'],r,methods=opts['methods'])
    return
