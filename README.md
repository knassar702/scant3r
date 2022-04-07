MAKE SURE TO READ THIS:  https://github.com/knassar702/scant3r/discussions/49


anyway you can try our XSS Scanner by using this command

```bash
$ cat urls.txt
http://testphp.vulnweb.com/listproducts.php?cat=1

$ cargo r -- scan --urls urls.txt
```

DONE:
* XSS Scanner ( with ATTRNAME | VALUE | Normal TEXT | TagName )
