#!/usr/bin/env python3
from libs import NewRequest as nq
from libs import post_data
from threading import Thread
from queue import Queue
from random import randint
from core import info,good
from urllib.parse import urlparse

t = Queue()

def reflect(link):
    try:
        for parameter in link.split('?')[1].split('&'):
            newparameter = f'sca{randint(1,20)}nt3r'
            newlink = link.replace(parameter,parameter+newparameter)
            r = nq.Get(newlink)
            if r != 0:
                if newparameter in r.content.decode('utf-8'):
                    print(f'''
{good} Relfected > {newlink} 
{info} Parameter > {parameter}
{info} Text > {newparameter}
''')
                else:
                    continue
    except:
        pass
    finally:
        pass

def threader():
    while True:
        item = t.get()
        reflect(item)
        t.task_done()

def run(opts):
    for _ in range(opts['threads']):
        p1 = Thread(target=threader)
        p1.deamon = True
        p1.start()
    for url in opts['url']:
        t.put(url)
    t.join()
