#!/usr/bin/env python3
import re

class Colors:
    # normal colors
    red = '\u001b[31m'
    rest = '\u001b[0m'
    black = '\u001b[30m'
    green = '\u001b[32m'
    yellow = '\u001b[33m'
    grey = "\x1b[38;21m"
    blue = '\u001b[34m'
    magenta = '\u001b[35m'
    cyan = '\u001b[36m'
    white = '\u001b[37m'
    # Bright Colors
    bblack = '\u001b[30;1m'
    bred = '\u001b[31;1m'
    bgreen = '\u001b[32;1m'
    byellow = '\u001b[33;1m'
    bblue = '\u001b[34;1m'
    bmagenta = '\u001b[35;1m'
    bcyan = '\u001b[36;1m'
    bwhite = '\u001b[37;1m'
    # Background Colors
    Bblack = '\u001b[40m'
    Bred = '\u001b[41m'
    Bgreen = '\u001b[42m'
    Byellow = '\u001b[43m'
    Bblue = '\u001b[44m'
    Bcyan = '\u001b[46m'
    Bwhite = '\u001b[47m'
    BBblack = '\u001b[40;1m'
    BBred = '\u001b[41;1m'
    BBgreen = '\u001b[42;1m'
    BByellow = '\u001b[43;1m'
    BBblue = '\u001b[44;1m'
    BBmagenta = '\u001b[45;1m'
    BBcyan = '\u001b[46;1m'
    BBwhite = '\u001b[47;1m'
    # idk
    good = f'{yellow}[{rest}{green}+{rest}{yellow}]{rest}'
    bad = f'{yellow}[{rest}{red}-{rest}{yellow}]{rest}'
    info = f'{yellow}[{yellow}!{rest}{yellow}]{rest}'
    
def dump_colors():
    ac = {}
    for c,v in vars(Colors).items():
        if len(re.findall(r'__.*.',c)) == 0:
           ac[c] = v
    return ac
