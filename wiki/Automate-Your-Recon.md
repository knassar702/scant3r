while doing bug bounty hunting, you need to automate your work by running your recon tools from bash script but bash is not useful, you need to wait for every domain to finish his work, in scant3r you can run multi-tools on more than one domain for making it faster

### Steps:
* add your tools in `modules/exec/conf.yaml`
```yaml

subdomain enum:
    sublist3r: python3 ~/sublist3r.py -d 
    subfinder: subfinder -d 

geturls:
    waybackurls: waybackurls
    gau: gau

# Process Name:
#    TOOL NAME: command
```

### How can I pass my scant3r options to these tools .?
* basically add the option name in command line between {}

for example

```
subdomain enum:
    assetfinder: assetfinder -subs-only {domain}
geturls:
    waybackurls: waybackurls {url} -t {timeout}
```



* Download your tools and add it 

#### Run

```
$ cat domains.txt
vulnweb.com

$ cat domains.txt | ./scant3r.py -m exec

   ____              __  ____
  / __/______ ____  / /_|_  /____
 _\ \/ __/ _ `/ _ \/ __//_ </ __/
/___/\__/\_,_/_//_/\__/____/_/

[!] Coded by: Khaled Nassar @knassar702
[!] Version: 0.7#Beta

mx0.vulnweb.com
wpmulti1.vulnweb.com
www.wpmulti1.vulnweb.com
mx1.vulnweb.com
gd2.vulnweb.com
wsdtest2.vulnweb.com
gd3.vulnweb.com
testmetasploitable.vulnweb.com
http://testphp.vulnweb.com/showimage.php?file=8
http://testphp.vulnweb.com/showimage.php?file=8&size=160
http://testphp.vulnweb.com/showimage.php?file=vuln8&size=160
......
......

```