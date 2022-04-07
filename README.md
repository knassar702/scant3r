MAKE SURE TO READ THIS:  https://github.com/knassar702/scant3r/discussions/49


anyway you can try our XSS Scanner by using this command

```bash
$ cat urls.txt
http://testphp.vulnweb.com/listproducts.php?cat=1

$ cargo r -- scan --urls urls.txt
FOUND XSS
Reflect: Text("\n\tError: Unknown column 'hackerman' in 'where clause'\nWarning: mysql_fetch_array() expects param
eter 1 to be resource, boolean given in /hj/var/www/listproducts.php on line 74\n")
Payload: "\"><img src=x onerror=alert`1`>"
Match: "<img onerror=\"alert`1`\" src=\"x\">"
```

DONE:
* XSS Scanner ( with ATTRNAME | VALUE | Normal TEXT | TagName )
