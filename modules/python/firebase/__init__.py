from .firebase import Firebase

def main(opts,http):
    Firebase(opts,http).start()
