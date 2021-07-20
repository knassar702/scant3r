from .finder import Finder

def main(opts, http):
    return Finder(opts, http).start() 
