from .exec import Scan

def main(opts, http):
    m = Scan(opts).run()
