
from vuln import methods

def main(opts):
    r = methods.Post(opts['url'],'')
    print(r)
