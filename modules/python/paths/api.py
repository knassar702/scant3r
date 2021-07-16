#!/usr/bin/env python3
from .paths import start

def main(opts,msg):
    m = start(opts['url'],msg)
    return m
