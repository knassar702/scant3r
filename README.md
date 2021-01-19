# Scant3r - web application vulnerability scanner

**Why would you use Scant3r?**

Scant3r Scans all URLs with multiple HTTP Methods and Tries to look for bugs with basic exploits as **XSS - SQLI - RCE - CRLF -SSTI** from Headers and URL Parameters
By chaining [waybackurls](https://github.com/tomnomnom/waybackurls) or [gau](https://github.com/lc/gau) <br>
with Scant3r you will have more time to look into functions and get Easy bugs on the way :)

### What will Scant3r give you?

**Scant3r will give you more time to focus on functionalities We've provided some modules to help you**

| Module              | Description                   |
| :-------------    | :-------------                |
| **lorsrf** | Bruteforcing on Hidden parameters to find SSRF vulnerability |
| **hostping** | get live domains|
| **hostinj** | Host Header injection |
| **paths** | dirbrute forcing|
| **reflect** | find reflected parameters|
| **headers** | add your payloads in HTTP headers | 
| **neon** | scans admin panel from CVE-2019-20141 |

**If you want to write your own module**
* https://github.com/knassar702/scant3r/wiki/writing-your-own-scant3r-module

***
## Installation

### Linux ![Linux](http://icons.iconarchive.com/icons/dakirby309/simply-styled/32/OS-Linux-icon.png)

```bash
$ git clone https://github.com/knassar702/scant3r
$ cd scant3r
$ pip3 install -r requirements.txt
```

#### Update to latest version:
```bash
$ cd scant3r
$ git pull
```
### Usage
* https://github.com/knassar702/scant3r/wiki/Usage
### ScanT3r API
* https://github.com/knassar702/scant3r/wiki/ScanT3r-API


### Demo 

![Example](images/all.gif)

**Nokia** https://www.nokia.com/responsible-disclosure/
![Nokia](images/nokia.gif)

**IBM** https://hackerone.com/ibm

![IBM](images/ibm.png)

