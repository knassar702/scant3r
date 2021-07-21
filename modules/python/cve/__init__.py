from .cve import Cve


def main(opts,http):
    Cve(opts,http).start()
