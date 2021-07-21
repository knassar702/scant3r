#!/usr/bin/env python3
from .secrets import Secrets
from core.libs import Http

def main(opts: dict, http: Http):
    Secrets(opts, http).start()
