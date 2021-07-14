when writing your own python script, you need to learn to adjust threading,option parser and fixing connection errors etc.. in scant3r all you have to do is to write main function and scant3r will organize all issues (threads,errors,etc..) you will find some functions that'll help you to write a greate module 😃

***

### Steps:
* write main funcation with opts argument:D
```python
def main(opts,http):
   print(opts)
```
and save it in `modules/example/__init__.py`

>> 
* opts = all scant3r options
* http = scan http module with user configuration

```python
$ echo http://127.0.0.1:5000/ | ./scant3r.py -R -m example -w 100

{'proxy': None,
   'timeout': 10,
   'Headers': {},
   'list': None,
   'random-agent': True,
   'threads': 100,
   'module': ['example'],
   'url': 'http://127.0.0.1:5000/',
   'host': None}
```
to fetch option just add `opts['OPTION']` for example `opts['url']`

* run your module
`$ echo 'http://google.com/' | python3 scant3r.py -m youmodulename`

## all scant3r functions

#### Data Parsing : `core/libs/all/data.py`
* import: `from core.libs import YOUR_FUNC`

| function              | Description                   | example |
| :-------------    | :-------------                | :-------------                | 
| post_data | add string value to dictionary (for cookies,post/put parameters) | post_data('name=khaled&id=444') > {'name':'khaled','id':44}|
| urlencoder | from plain text to url encoding| `urlencoder(yourtext,many=1)` > many = how many you want to encode your payloads|
| extractHeaders | add headers value to dictionary| `extractHeaders('Header: hello') > {'Header':'hello'}`|
| insertAfter | Insert some string into given string at given index |`insertAfter('scant3r','3r','test')` > scantest |
| random_str | make random string value by length | `random_str(5) > 3AQU5` | 
| remove_dups | remove duplicated items from the list | `remove_dups(['test','test']) > ['test']`| 
| dump_params | dump all parameters in your url| `dump_params('http://google.com/?test=1&hmm=2') > 'test=1&hmm=2'`|
| add_path | add path to your url | `add_path('http://google.com/','/hackerman') > http://google.com/hackerman` |
| alert_bug | bug alert | alert_bug('XSS',http,payload='<xss>',bruhh='yes')
| insert_to_params_urls | add a string to url parameters | `insert_to_params_urls('http://google.com/?test=1&hi=vv','scant3r')` > `['http://google.com/?test=1scant3r&hi=vv','http://google.com/?test=1&hi=vvscant3r']`| 
| insert_to_params | add parameters to url |`insert_to_params('http://php.net/?test=1','man=1') > http://php.net/?test=1&hi=3` |
| dump_request | dump http request | `dump_request(r) # r = requests module`
| dump_response | dump http response | `dump_response(r) # r = requests module`



***
### Options Parsing : `core/libs/all/args.py`
args.py load all options from `core/settings/opts.yaml` file

### Colors: `core/libs/all/colors.py`

### http requests: core/libs/all/requester.py

| function              | Description                   |
| :-------------    | :-------------                |
| Agent | get random user agents from `wordlists/agents.txt`|
| http | send http requests module|


#### post_data
```python
>> from core.libs import post_data
>> post_data('id=1&user=admin')

{
  'id':'1',
  'user':'admin'
}
```
#### http
you don't need to import http module just add `r` argument in your main function
```python
from core.libs import extractHeaders
# send : send http request with scant3r options (-H -p etc ..)
# custom : send http request with your options (function parameters)
def main(opts,r):
   req = r.send('GET','https://httpbin.org/get')
   # req = r.custom('POST','http://httpbin.org/post',headers=extractHeaders('test: hello'),body='test=1444')
   print(req.content.decode('utf-8'))
```
##### extractHeaders
```python
>> from core.libs import extractHeaders
>> headers = '''
Auth: c2NhbnQzcgo=
Host: knassar702.github.io
'''
>> extractHeaders(headers)
{'Auth': 'c2NhbnQzcgo=',"Host":"knassar702.github.io"}
```
##### urlencoder
```python
>> from core.libs import urlencoder
>> urlencoder('<',1)
%3c
%3c <
>> urlencoder('<',2)
%25%33%63
# %25%33%63 > %3c > <
```
#### insertAfter
```python
>> from core.libs import insertAfter
insertAfter('TEXT','INSERT_AFTER','NewText')

>> insertAfter('http://site.com/?msg=hi','=','<svg/onload=alert(1)>')
http://site.com/?msg=<svg/onload=alert(1)>
```

#### Colors
```python
>> from core.libs import dump_colors
>> 
>> dump_colors()
{
   "red":"\\x1b[31m",
   "rest":"\\x1b[0m",
   "black":"\\x1b[30m",
   "green":"\\x1b[32m",
   "yellow":"\\x1b[33m",
   "blue":"\\x1b[34m",
   "magenta":"\\x1b[35m",
   "cyan":"\\x1b[36m",
   "white":"\\x1b[37m",
   "bblack":"\\x1b[30;1m",
   "bred":"\\x1b[31;1m",
   "bgreen":"\\x1b[32;1m",
   "byellow":"\\x1b[33;1m",
   "bblue":"\\x1b[34;1m",
   "bmagenta":"\\x1b[35;1m",
   "bcyan":"\\x1b[36;1m",
   "bwhite":"\\x1b[37;1m",
   "Bblack":"\\x1b[40m",
   "Bred":"\\x1b[41m",
   "Bgreen":"\\x1b[42m",
   "Byellow":"\\x1b[43m",
   "Bblue":"\\x1b[44m"
}

>>> >>> print(f"{dump_colors()['good']} Yes")
[+] Yes
```

Thanks