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
__author__ = 'Khaled Nassar'
__version__ = '0.4#beta'
__github__ = 'https://github.com/knassar702/scant3r'
__email__ = 'knassar702@gmail.com'
__blog__ = 'https://knassar7o2.blogspot.com'
from datetime import datetime
from .colors import *
from .config import *
from .logger import logger
from .scanner import uagent
from time import sleep
from urllib.parse import urlparse
import requests
requests.packages.urllib3.disable_warnings()
def thetime():
	now = datetime.now()
	return f'{bold}{blue}[{end}{bold}{now.hour}:{now.minute}:{now.second}{blue}{bold}]{end}'
def red(w):
	if w == 'ag':
		return True
	else:
		return False
def con(url,redir,cookie=None,timeo=None,proxy=None,slp=0,cagent=None):
	try:
		sleep(slp)
		r = requests.get(url,allow_redirects=redir,timeout=timeo,cookies=cookie,verify=False,proxies=proxy,headers={'User-agent':uagent(cagent=cagent)})
		try:
			v = r.headers['server']
			v = f'[{v}]'
		except:
			v = '[]'
		print(f'''
{info} {bold}Host {end}: {urlparse(url).netloc}
{info} {bold}Status Code {end}: {r.status_code}
{info} {bold}Server {end}: {v}
			''')
		if r.status_code == 999:
			sleep(1)
	except requests.exceptions.ConnectionError:
		print(f"{bad} host '{blue}{url}{end}' does not exist ..!")
		exit()
	except requests.exceptions.ReadTimeout:
		print(f"\n{bad} Timeout Error ")
		exit()
	except requests.exceptions.ProxyError:
		print(f"{bad} Proxy Connection Error")
		exit()
	except requests.exceptions.InvalidURL:
		print(f"{bad} Invalid URL")
		exit()
	except requests.exceptions.InvalidSchema:
		print(f"{bad} Invalid Schame")
		exit()
	except requests.exceptions.MissingSchema:
		print(f"{bad} Missing Schema")
		exit()
def con_f(url,redir,cookie=None,timeo=None,proxy=None,cagent=None,slp=0):
	try:
		sleep(slp)
		r = requests.get(url,allow_redirects=redir,timeout=timeo,verify=False,cookies=cookie,proxies=proxy,headers={'User-agent':uagent(cagent=cagent)})
		return 'ok'
	except requests.exceptions.ReadTimeout:
		return 'no','\ntimeout error ..'
	except requests.exceptions.ConnectionError:
		return 'no','Connection Error ..'
	except requests.exceptions.ProxyError:
		return 'no','Proxy Connection Error'
	except requests.exceptions.InvalidURL:
		return 'no','Invalid URL'
	except requests.exceptions.InvalidSchema:
		return 'no','Invalid Schema'
	except requests.exceptions.MissingSchema:
		return 'no','Missing Schema'
