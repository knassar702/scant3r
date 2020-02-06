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
from .scanner import uagent
from time import sleep
import requests,urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
__author__ = 'Khaled Nassar'
__version__ = '0.2#beta'
__github__ = 'https://github.com/knassar702/scant3r'
__email__ = 'knassar702@gmail.com'
__blog__ = 'https://knassar7o2.blogspot.com'
def thetime():
	now = datetime.now()
	return f'{bold}{blue}[{end}{bold}{now.hour}:{now.minute}:{now.second}{blue}{bold}]{end}'
def red(w):
	if w == 'ag':
		return True
	else:
		return False
def printer(what,msg):
	if what == 'info':
		print(thetime()+f' [{green}INFO{end}] {msg}')
	elif what == 'error':
		print(thetime()+f' [\033[91m{bold}CRITICAL{end}] {msg}')
	elif what == 'war':
		print(thetime()+f' [{yellow}{bold}WARRING{end}] {msg}')
	elif what == 'qu':
		p = input(msg)
		if 'Y' in p or 'y' in p:
			pass
		else:
			exit()
def con(url,redir,cookie=None,timeo=None,vert=None,proxy=None,slp=0,cagent=None):
	try:
		sleep(slp)
		r = requests.get(url,allow_redirects=redir,timeout=timeo,cookies=cookie,verify=vert,proxies=proxy,headers={'User-agent':uagent(cagent=cagent)})
		if r.status_code == 200:
			for h,v in r.headers.items():
				if h == 'Server':
					server = v
					break
			print(f"""
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}
{bold}{info}{bold} Status Code : {green}{r.status_code}{end}
{bold}{info}{bold} Host : {url.split('/')[2]}
{bold}{info}{bold} Web Server : {server}
{bold}{info}{bold} Encoding  : {r.encoding}
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}
					""")
		elif r.status_code == 302 or r.status_code == 301:
			printer('qu',f'ScanT3r got a {r.status_code} redirect to another website. Do you want to contiune .? [y/n] ')
		elif r.status_code == 999:
			printer("info",'Detect KingWaf Firwill')
			sleep(1)
	except requests.exceptions.ConnectionError:
		printer('error',f"host '{blue}{url}{end}' does not exist ..!")
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
def con_f(url,redir,cookie=None,timeo=None,vert=None,proxy=None,cagent=None,slp=0):
	try:
		sleep(slp)
		r = requests.get(url,allow_redirects=redir,timeout=timeo,verify=vert,cookies=cookie,proxies=proxy,headers={'User-agent':uagent(cagent=cagent)})
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
