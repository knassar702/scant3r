hello ,
here my module file
```
example
├── api.py
├── funcs.py
└── __init__.py
```
* `funcs.py`
```python

def check(opts,r):
   req = r.send('GET',opts['url'])
   if 'welcome to our page' in req.content.decode('utf-8'):
      c = {'Found':opts['url']}
   else:
      c = {}
   return c
```
* `__init__.py`
```python
from .funcs import check

def main(opts,r):
   hm = check(opts,r)
   if hm:
      print('Found:>' + hm['Found'])
```
* `api.py`

```python3
from .funcs import check

def main(opts,r):
   return check(opts,r)
```

run `./scant3r.py -a`

![ScanT3r-api](https://github.com/knassar702/scant3r/blob/master/.src/scant3r_api.png)

Access your module 
`$ curl -X POST --data-urlencode "url=http://testphp.vulnweb.com" http://localhost:6030/scan/{scanid} `

```
$ curl -X POST --data-urlencode "url=http://testphp.vulnweb.com" http://localhost:6030/scan/2

{
  "Results": {
    "Found": "http://testphp.vulnweb.com"
  }
}

```