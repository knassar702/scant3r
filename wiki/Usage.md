* Normal
```bash
echo yourtarget.com | ./scant3r.py -m module,module2
```

  
```bash
$ cat yourtargets.txt | ./scant3r.py -m injheaders -b yourxssht.xss.ht
```

***

* random User-agents
```bash
$ echo "http://testphp.vulnweb.com/search.php?test=query&searchFor=1&goButton=go" | python3 scant3r.py -R
```
* add custom headers
```bash
$ echo "http://testphp.vulnweb.com/search.php?test=query&searchFor=1&goButton=go" | python3 scant3r.py -H "Auth: U2NhblQzcgo=\nNew: True"
```
* check the target with theses methods
```bash
$ echo 'http://python.org' | ./scant3r.py -y GET,POST,PUT -m xss,injheaders
```
* add timeout
```bash
$ echo "http://testphp.vulnweb.com/search.php?test=query&searchFor=1&goButton=go" | python3 scant3r.py -t 1000
```
* add threads
```bash
$ echo "http://testphp.vulnweb.com/search.php?test=query&searchFor=1&goButton=go" | python3 scant3r.py -w 50
```
* add proxy
```bash
$ echo "http://testphp.vulnweb.com/search.php?test=query&searchFor=1&goButton=go" | python3 scant3r.py -p http://localhost:8080
```
* follow redirects
```bash
$ echo "http://testphp.vulnweb.com/search.php?test=query&searchFor=1&goButton=go" | python3 scant3r.py -r
```
* dump http requests/responses
```bash
$ echo "http://testphp.vulnweb.com/search.php?test=query&searchFor=1&goButton=go" | python3 scant3r.py -H "Auth: U2NhblQzcgo=" -d
```

* remove banner
```bash
$ echo "http://testphp.vulnweb.com/search.php?test=query&searchFor=1&goButton=go" | python3 scant3r.py -n```
