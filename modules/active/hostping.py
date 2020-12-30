#!/usr/bin/env python3
from socket import gethostbyname as ping
from queue import Queue
from threading import Thread

q = Queue()

def start(host):
    try:
        host = host.replace('http://','').replace('https://','')
        HOST = ping(host)
        print(f'{host} {HOST}')
    except:
        pass

def main(opts):
    start(opts['url'])