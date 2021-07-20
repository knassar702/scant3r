from .xss_param import XssParam

def main(opts,r):
    return XssParam(opts,r).start()
