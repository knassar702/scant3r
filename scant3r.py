#!/usr/bin/env python
import time,sys,os,logging,re
from core.scanner import *
from core.colors import *
from optparse import OptionParser 
def cookie_list(params):
    if params:
        prePostData = params.split("&")
        postData = {}
        for d in prePostData:
            p = d.split("=", 1)
            postData[p[0]] = p[1]
        return postData
    return {}

def getargs():
	global url,froms,data,rfile,r,cookie
	r=False
	optp = OptionParser('')
	optp.add_option("-u","--url",dest="url",help='Target URL (e.g. "http://www.target.com/vuln.php?id=1")')
	optp.add_option("-d","--data",dest="data",help='Data string to be sent through POST (e.g. "id=1")')
	optp.add_option("-f","--forms",dest="forms",help="Parse and test forms on target URL")
	optp.add_option("-l","--list",dest="rfile",help="Get All Urls from file ..")
	optp.add_option("-c","--cookies",dest='cookie',help='Add cookie in Request')
	opts, args = optp.parse_args()
	if opts.url != None and opts.data == None and opts.forms == None and opts.rfile == None:
		url=opts.url
	if opts.url == None and opts.rfile != None:
		rfile=str(opts.rfile)
		r=True
	if opts.url != None and opts.rfile != None:
		print (mns+" You Can't Start ScanT3r With List and url option ")
		sys.exit()
	if opts.cookie:
		cookie=str(opts.cookie)
		cookie=cookie_list(cookie)
	else:
		cookie=None
	if opts.url == None:
		optp.error('missing a mandatory option (--url,--cookies,--data,--list,--random-agent) Use -h for help ..!')
		exit()

def logo():
	l=(f'''{red}{bold}
\t   _____                ___________     
\t  / ___/_________ _____/_  __/__  /_____
\t  \__ \/ ___/ __ `/ __ \/ /   /_ </ ___/
\t ___/ / /__/ /_/ / / / / /  ___/ / /    
\t/____/\___/\__,_/_/ /_/_/  /____/_/
\t
\t{yellow}# Coded By : Khaled Nassar @knassar702
''')
	print (l)
	time.sleep(1)
if __name__ == "__main__":
	try:
		logo()
		v=from_url_get()
		getargs()
		if url.startswith('http://') or url.startswith('https://'):
			pass
		else:
			url='http://'+url
		if '?' in url or '*' in url:
			pass
		else:
			print(f"{bad} Please Add parameters in url ..")
			exit()
		if r==True:
			rfile=open(rfile,'r')
			for url in rfile:
				url=url.strip()
				v.xss(url,cookie)
				v.sqli(url,cookie)
				v.osinj(url,cookie)
				v.ssti(url,cookie)
		else:
				v.sqli(url,cookie)
				v.xss(url,cookie)
				v.osinj(url,cookie)
				v.ssti(url,cookie)
	except KeyboardInterrupt:
		print(f'\n{bad} Good Bye :)\n')
		exit()
