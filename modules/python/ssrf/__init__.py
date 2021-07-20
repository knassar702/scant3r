from .ssrf import Ssrf

def main(opts, http):
    return Ssrf(opts, http).start()
    
