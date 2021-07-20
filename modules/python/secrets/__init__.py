#!/usr/bin/env python3
from .secrets import Secrets

def main(opts, r):
    Secrets(opts, r).start()
