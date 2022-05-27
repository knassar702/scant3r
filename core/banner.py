from core.data import console, LOGO
import time
 

def display_banner(*args):
    console.print(LOGO)
    msg = ""
    for option in args:
        msg += "\n%s" %option
    console.print(msg)
    time.sleep(2)
