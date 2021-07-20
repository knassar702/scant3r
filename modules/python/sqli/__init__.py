from .sqli import Sqli

def main(opts, http):
    c = Sqli(opts, http).start()
    # C is always an empty dict
    if c:
        return c 