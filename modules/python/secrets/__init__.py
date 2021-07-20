#!/usr/bin/env python3
from .secrets import Secrets

def main(opts, http):
    Secrets(opts, http).start()
