#!/usr/bin/env python3
from logging import getLogger
from modules import Scan
from importlib import import_module
from glob import glob
from urllib.parse import urljoin
from core.libs import alert_bug
import concurrent.futures
from core.libs import Http
from .loader import python_loader, yaml_loader
import re 

log = getLogger('scant3r')

class Cve(Scan):
    def __init__(self, opts: dict, http: Http):
        super().__init__(opts, http)
    def start(self):
        python_loader(self)
        yaml_loader(self)
        return {}

