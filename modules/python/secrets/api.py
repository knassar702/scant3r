from .secrets import Secrets

def main(opts,r):
    return Secrets(opts, r).start()
