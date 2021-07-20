from .sqli import Sqli

def main(opts, r):
    c = Sqli(opts, r).start()
    # C is always an empty dict
    if c:
        return c 