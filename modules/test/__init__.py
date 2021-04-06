import time
from core.libs.all.console import log

def main(opts,r):
    logger = log()
    for i in range(10):
        #print(i)
        logger.error('Find man')
        print(f'Hello , for testing \n Your Options: {opts} ')
        # send http request
        # r.send('GET','http://example.com')
        time.sleep(0.6)
