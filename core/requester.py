#!/usr/bin/env python3
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
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
def con(url,redir,vert,cookie):
	try:
		r = requests.get(url,allow_redirects=redir,cookies=cookie)
		if r.status_code == 200:
			pass
		elif r.status_code == 302 or r.status_code == 301:
			printer('qu',f'ScanT3r got a {r.status_code} redirect to another website. Do you want to follow .? [y/n] ')
	except requests.exceptions.ConnectionError:
		printer('error',f"host '{blue}{url}{end}' does not exist ..!")
		exit()
