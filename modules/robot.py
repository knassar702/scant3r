#!/usr/bin/env python3
from modules.scant3r_maker import Module,colors,thetime
def data(): # The all data of module
	data = {
	'name': 'Robot Man',
	'description':'''
Find Robots File
	''',
	'date':'6-3-2020',
	'license':'GPL',
	'authors':[
	'Khaled Nassar'],
	'emails':[
	'knassar702@gmail.com'],
	'list_support': True,
	'options':[
	'url',
	'threads',
	'timeout'
	]
	}
	return data
class script:
	def __init__(self):
		global q
		from queue import Queue
		q = Queue()
	def threader():
		item = q.get()
		script.opener(item)
		q.task_done()
	def opener(domain):
		import requests
		try:
			if domain.strip().endswith('/'):
				ro = 'robots.txt'
			else:
				ro = '/robots.txt'
			r = requests.get(f'{domain.strip()}{ro}',timeout=timeout,verify=False,allow_redirects=False)
			if r.status_code == 200:
				print(f'{colors().good} Found : {r.url}')
				print(r.text)
				print('\n----------------------------\n')
		except:
			pass
#			print(f'{colors().bad} {domain.strip()}')
	def run(self,options):
		global timeout,name
		import os
		timeout = options['timeout']
		from threading import Thread
		for thr in range(options['threads']):
			p1 = Thread(target=script.threader)
			p1.daemon = True
			p1.start()
		for url in options['file']:
			q.put(url.strip())
		q.join()