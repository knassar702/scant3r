# Security Policy


### Scope

| ScanT3r Type | Supported          |
| ------- | ------------------ |
| API | :white_check_mark: |
| Console   | :white_check_mark:       

## Reporting a Vulnerability

I think I am too lazy to test my tool, so if you find any security risk (low/high etc ..) , share it with me  <br>
you can open issue with `bug_report.md` template , or send mail to `knassar702@gmail.com`

When sending the report please add what damage will be caused by this security issue

for example

***
Title: [ScanT3r API] SSRF in scant3r api <br>
Type: SSRF <br>
Description : [description of bug] <br>
Steps:
* one
* two
* three

```python
# exploit script
import requests
r = requests.get('https://knassar702.github.io')
if 'knassar702.github.io' in r.content.decode():
    print('HACKED')
```

Reference: https://owasp.org/www-community/attacks/Server_Side_Request_Forgery
