To find blind XSS vulnerability you need to inject your payload to `headers/parameters name & values` so scant3r support

## Parameters
```
$ cat urls.txt | ./scant3r.py -m xss -b yourxssht.xss.ht
```

## Headers
first write the headers you wan't to scan in `modules/injheaders/headers.yaml`

```yaml
"User-agent": "Mozilla/5.0 (Macintosh; U; PPC Mac OS X; de-de) AppleWebKit/125.2 (KHTML, like Gecko) Safari/125.7"
"Refere": 'http://google.com'
```
run it
```
$ cat urls.txt | ./scant3r.py -m injheaders -b yourxssht.xss.ht
```


* inject (b)xss in `[ parameters value & name , headers`

```bash
$ cat urls.txt | ./scant3r.py -m xss,xss_param,injheaders -b example.xss.ht -w 100
```
