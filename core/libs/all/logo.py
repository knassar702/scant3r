#!/usr/bin/env python3
__author__ = 'Khaled Nassar'
__email__ = 'knassar702@gmail.com'
__version__ = '0.8#Beta'

from glob import glob
from .colors import dump_colors
import random

# Print one random logo
def logo():
    logos = []
    for logo in glob('conf/logo/*.txt'):
        logos.append(open(logo,'r').read().format(**dump_colors())) 
    print(random.choice(logos))

