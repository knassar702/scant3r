#!/usr/bin/env python3
__name__ = 'ScanT3r'
__author__ = 'Khaled Nassar'
__email__ = 'knassar702@gmail.com'
__version__ = '0.5#Beta'

from datetime import datetime
from .colors import *
import random
def logo():
    logos = [f"""
{red}
   ____              __  ____
  / __/______ ____  / /_|_  /____
{yellow} _\ \/ __/ _ `/ _ \/ __//_ </ __/
{green}/___/\__/\_,_/_//_/\__/____/_/{rest}
""",r"""{red}
+-+-+-+-+-+-+-+
|S|C|a|N|t|3|r|
+-+-+-+-+-+-+-+{red}
             ____
            / . .\
            \  {cyan}---<{red}
             \  /
   __________/ /
-=:___________/""".format(red=red,cyan=cyan).replace('+',f'{green}+{yellow}')
	,r"""{red}
 ___          _  _ _____ ____    
/ __| __ __ _| \| |_   _|__ /_ _ 
\__ \/ _/ _` {green}| {green}.` | | |  {cyan}|_ \ '_|
|___/\__\__,_|_|\_| {green}|_| {cyan}|___/_|""".format(red=red,cyan=cyan,green=green)
    ]
    print(random.choice(logos))
    print(f'''
{info} Coded by : Khaled Nassar @knassar702
{info} Version : 0.5#Beta
    	''')