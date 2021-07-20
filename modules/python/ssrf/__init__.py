from .ssrf import Ssrf

def main(opts,r):
    return Ssrf(opts, r).start()
    
