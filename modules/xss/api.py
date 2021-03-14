from .xss import Scan



def main(url,opts,r):
    opts['url'] = url
    scanner = Scan(opts,r)
    return scanner.start(opts['url'],methods=['GET','POST','PUT'])
