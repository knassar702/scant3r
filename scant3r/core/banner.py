import time

from scant3r.core.data import LOGO, console


def display_banner(*args):
    console.print(LOGO)
    msg = ""
    for option in args:
        msg += "\n%s" % option
    console.print(msg)

    time.sleep(1)
