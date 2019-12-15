#!/usr/bin/env python
from datetime import datetime
from .colors import *
from .config import *
import requests
def thetime():
	now = datetime.now()
	return f'{bold}{blue}[{end}{bold}{now.hour}:{now.minute}:{now.second}{blue}{bold}]{end}'
def printer(what,msg):
	if what == 'info':
		print(thetime()+f' [{green}INFO{end}] {msg}')
	elif what == 'error':
		print(thetime()+f' [{red}{bold}CRITICAL{end}] {msg}')
	elif what == 'war':
		print(thetime()+f' [{yellow}{bold}WARRING{end}] {msg}')
	elif what == 'qu':
		p = input(msg)
		if 'Y' in p or 'y' in p:
			pass
		else:
			exit()
def con(url):
	try:
		r = requests.get(url,allow_redirects=redir)
		if r.status_code == 200:
			pass
		elif r.status_code == 302 or r.status_code == 301:
			printer('qu',f'ScanT3r got a {r.status_code} redirect to another website. Do you want to follow .? [y/n] ')
	except requests.exceptions.ConnectionError:
		printer('error',f"host '{blue}{url}{end}' does not exist ..!")
		exit()
