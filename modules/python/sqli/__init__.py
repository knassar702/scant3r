from .sqli import Scan

def main(opts, r):
    s = Scan(opts, r)    
    c = s.scan()
    # C is always an empty dict
    if c:
        return c 