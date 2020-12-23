#!/usr/bin/env python3

from threading import Thread
from queue import Queue
from optparse import OptionParser
from urllib.parse import urlparse
import requests,sys,os,platform,re

colors = True  # Output should be colored
machine = sys.platform  # Detecting the os of current system
checkplatform = platform.platform() # Get current version of OS
if machine.lower().startswith(('os', 'win', 'darwin', 'ios')):
    colors = False  # Colors shouldn't be displayed in mac & windows
if checkplatform.startswith("Windows-10") and int(platform.version().split(".")[2]) >= 10586:
    colors = True
    os.system('')   # Enables the ANSI
if not colors:
    end = red = white = green = yellow = run = bad = good = bold = info = que = ''
else:
    white = '\033[97m'
    green = '\033[92m'
    red = '\033[91m'
    yellow = '\033[93m'
    end = '\033[0m'
    back = '\033[7;91m'
    bold = '\033[1m'
    blue = '\033[94m'
    info = '\033[93m[!]\033[0m'
    que = '\033[94m[?]\033[0m'
    bad = '\033[91m[-]\033[0m'
    good = '\033[92m[+]\033[0m'
    run = '\033[97m[~]\033[0m'
    grey = '\033[7;90m'
    cyan='\u001B[36m'
    gray = '\033[90m'

requests.packages.urllib3.disable_warnings()

def post_data(params):
    if params:
        prePostData = params.split("&")
        postData = {}
        for d in prePostData:
            p = d.split("=", 1)
            postData[p[0]] = p[1]
        return postData
    return {}
def extractHeaders(headers):
    headers = headers.replace('\\n', '\n')
    sorted_headers = {}
    matches = re.findall(r'(.*):\s(.*)', headers)
    for match in matches:
        header = match[0]
        value = match[1]
        try:
            if value[-1] == ',':
                value = value[:-1]
            sorted_headers[header] = value
        except IndexError:
            pass
    return sorted_headers
print('''
{red}{bold}
\t _            ___      __ 
\t| |   ___ _ _/ __|_ _ / _|
\t| |__/ _ \ '_\__ \ '_|  _|
\t|____\___/_| |___/_| |_|  
\t
\t{yellow}{bold}# Coded By : Khaled Nassar @knassar702
{end}
	'''.format(red=red,bold=bold,yellow=yellow,end=end))
optp = OptionParser(add_help_option=False)
optp.add_option('-t',dest='target')
optp.add_option('-h','--help',dest='help',action='store_true')
optp.add_option('-s',dest='server')
optp.add_option('-c','--cookies',dest='cookies')
optp.add_option('--timeout',dest='timeout',type='int')
optp.add_option('-r','--allow_redirects',dest='redirect',action='store_true')
optp.add_option('--threads',dest='threads',type='int')
optp.add_option('-w',dest='wordlist')
optp.add_option('-f',dest='hf')
opts, args = optp.parse_args()
helper = f"""
Options:
	-h         | show help message and exit
	-w         | add your wordlist
	-t         | your target
	-s         | your host
	-c         | add cookies
	-f         | headers file
	-r         | allow redirects
	--threads  | add threads
	--timeout  | add timeout

Example:
	$ cat parameter.txt | python3 lorsrf.py -t http://example.com/ -s http://host
"""
if opts.help:
	print(helper)
	sys.exit()
if opts.wordlist:
	wordlist = opts.wordlist
	try:
		f = open(wordlist,'r')
	except Exception as e:
		print(e)
		sys.exit()
else:
	wordlist = None
if opts.threads:
	thr = opts.threads
else:
	thr = 10
if opts.target:
	link = opts.target
else:
	print(helper)
	sys.exit()
if opts.server:
	host = opts.server
else:
	print(helper)
	sys.exit()
if opts.hf:
	try:
		hf = open(opts.hf,'r')
		HF = extractHeaders(hf.read())
	except Exception as e:
		print(f'{bad} Error: {e}')
		sys.exit()
else:
	HF = None
if opts.cookies:
	c = post_data(opts.cookies)
else:
	c = None

if opts.redirect:
	redirect = True
else:
	redirect = False
if opts.timeout:
	timeout = opts.timeout
else:
	timeout = None
def req(link,cookie=None,redirect=None,header={},timeout=None):
	try:
		if header:
			r = requests.get(link,verify=False,headers=header,allow_redirects=redirect,timeout=timeout,cookies=cookie)
			o = urlparse(link)
			r2 = requests.post(link.split('?')[0],verify=False,headers=header,allow_redirects=redirect,timeout=timeout,cookies=cookie,data=post_data(o.query))
		else:
			r = requests.get(link,verify=False,allow_redirects=redirect,timeout=timeout,cookies=cookie)
			o = urlparse(link)
			r2 = requests.post(link.split('?')[0],verify=False,allow_redirects=redirect,timeout=timeout,cookies=cookie,data=post_data(o.query))			
	except Exception as e:
		print(f'{bad} Error: {e}')
q = Queue()
def threader():
	while True:
		item = q.get()
		req(item,redirect=redirect,timeout=timeout,header=HF,cookie=c)
		q.task_done()

if __name__ == '__main__':
	for i in range(thr):
		p1 = Thread(target=threader)
		p1.daemon = True
		p1.start()
	if wordlist:
		for parameter in f:
			parameter = parameter.rstrip()
			q.put(f'{link}?{parameter}={host}/{parameter}')
	else:
		for parameter in sys.stdin:
			parameter = parameter.rstrip()
			q.put(f'{link}?{parameter}={host}/{parameter}')
	q.join()
