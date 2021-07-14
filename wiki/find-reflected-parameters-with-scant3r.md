if you want to check for XSS without inject XSS payloads , you need to find reflected parameters, so scant3r support that with reflect module

```bash
$ echo http://google.com/search?q= |./scant3r.py -m reflect -n
# you can add more methods 
# ./scant3r.py -m reflect -n -y GET,POST,PUT

[Refelct] Found :> {'http://google.com/search?q=scanHBDtr': 'GET'}

```