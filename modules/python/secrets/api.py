from . import Findme


def main(opts,r):
    c = Findme(opts,r)
    return c.start()
