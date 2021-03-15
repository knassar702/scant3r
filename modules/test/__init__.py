import time


def main(opts,r):
    for i in range(10):
        #print(i)
        print(f'Hello , for testing \n Your Options: {opts} ')
        # send http request
        # r.send('GET','http://example.com')
        time.sleep(0.6)
