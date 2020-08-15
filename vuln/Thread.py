#!/usr/bin/env python3
from vuln import Xss,Sqli,RCE,SSTI
from threading import Thread
from queue import Queue

def tsqli(q):
    while True:
        item = q.get()
        Sqli.Get(item)
        Sqli.Post(item)
        Sqli.Put(item)
        q.task_done()
def tssti(q):
    while True:
        item = q.get()
        SSTI.Get(item)
        SSTI.Post(item)
        SSTI.Put(item)
        q.task_done()
def trce(q):
    while True:
        item = q.get()
        RCE.Get(item)
        RCE.Post(item)
        RCE.Put(item)
        q.task_done()
def txss(q):
    while True:
        item = q.get()
        Xss.Get(item)
        Xss.Post(item)
        Xss.Put(item)
        q.task_done()