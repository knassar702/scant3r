from .paths import Scan

def main(opts,http):
    Scan(opts, http).scan()
