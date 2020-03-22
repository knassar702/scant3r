__author__ = 'Khaled Nassar'
__version__ = '0.3#beta'
__github__ = 'https://github.com/knassar702/scant3r'
__email__ = 'knassar702@gmail.com'
__blog__ = 'https://knassar7o2.blogspot.com'
import sys
import os
import platform
colors = True  # Output should be colored
machine = sys.platform  # Detecting the os of current system
checkplatform = platform.platform() # Get current version of OS
if machine.lower().startswith(('os', 'win', 'darwin', 'ios')):
    colors = False  # Colors shouldn't be displayed in mac & windows
if checkplatform.startswith("Windows-10") and int(platform.version().split(".")[2]) >= 10586:
    colors = True
    os.system('')   # Enables the ANSI
if not colors:
    end = red = white = green = yellow = run = bad = good = bold = info = que = ''
else:
    white = '\033[97m'
    green = '\033[92m'
    red = '\033[91m'
    yellow = '\033[93m'
    end = '\033[0m'
    back = '\033[7;91m'
    bold = '\033[1m'
    blue = '\033[94m'
    info = '\033[93m[!]\033[0m'
    que = '\033[94m[?]\033[0m'
    bad = '\033[91m[-]\033[0m'
    good = '\033[92m[+]\033[0m'
    run = '\033[97m[~]\033[0m'
    grey = '\033[7;90m'
    cyan='\u001B[36m'
    gray = '\033[90m'
