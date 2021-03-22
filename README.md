<h1 align="center">
  <br>
  <a href="https://github.com/knassar702/scant3r"><img src="/.src/sccc.png" alt="ScanT3r"></a>
  <br>
  ScanT3r
  <br>
</h1>


**Why would you use Scant3r?**

Scant3r Scans all URLs with multiple HTTP Methods and Tries to look for bugs with basic exploits from Headers and URL Parameters By chaining waybackurls or gau
with Scant3r you will have more time to look into functions and get Easy bugs on the way :)




### Modules

| Module         | Description                                                  |
| :------------- | :-------------                                               |
| **lorsrf**     | Bruteforcing on Hidden parameters to find SSRF vulnerability |
| **ssrf**       | simple ssrf scanner                                          |
| **paths**      | Check for custom paths                                       |
| **xss**        | inject xss payload in parameter value                        |
| **sqli**       | simple sqli scanner                                          |
| **finder**     | text Matcher in request/response                                                              |
| **xss_param** | inject xss payload in parameter name
| **ssti** | simple server side template injection scanner |
| **injheaders** | inject blind xss and custom payloads in custom headers (headers.yaml&payload.yaml)
| **reflect** | find reflected parameters 

scant3r will help you to write your own python script faster , you don't need to configure http/threads/errors/options/etc... , just by writing main function in your script , you can run it in your terminal or access your script from api :D
#### Write module for API
* https://github.com/knassar702/scant3r/wiki/write-module-for-api

#### writing your own scant3r module

* https://github.com/knassar702/scant3r/wiki/writing-your-own-scant3r-module


#### Edite Scant3r Command line options

* https://github.com/knassar702/scant3r/wiki/edite-scant3r-command-options


***
## Installation

### Linux ![Linux](http://icons.iconarchive.com/icons/dakirby309/simply-styled/32/OS-Linux-icon.png)

```bash
$ git clone https://github.com/knassar702/scant3r
$ cd scant3r
$ pip3 install -r requirements.txt
$ ./scant3r.py -h
```

#### Usage
* https://github.com/knassar702/scant3r/wiki/Usage


#### how to find hidden SSRF Parameters by using scant3r
* https://github.com/knassar702/scant3r/wiki/how-to-find-hidden-SSRF-Parameters-by-using-scant3r

#### Find Reflected Parameters with scant3r 
* https://github.com/knassar702/scant3r/wiki/find-reflected-parameters-with-scant3r

#### How to Find sensitive files by using ScanT3r
* https://github.com/knassar702/scant3r/wiki/How-to-Find-sensitive-files-by-using-ScanT3r

#### Find Blind XSS With ScanT3r
* https://github.com/knassar702/scant3r/wiki/Find-Blind-XSS-with-scant3r

#### ScanT3r API
* https://github.com/knassar702/scant3r/wiki/ScanT3r-API


## TODOLIST
* add web spider
* send/analizy requests from .yaml file
* SSRF/SQLI/REC/SSTI Module



### Media 

### Version: 0.7
* XSS Scanner
[![asciicast](https://asciinema.org/a/ROYOYuR7u7Ebjc81gf9iqisfw.svg)](https://asciinema.org/a/ROYOYuR7u7Ebjc81gf9iqisfw)

* injheaders
[![asciicast](https://asciinema.org/a/400245.svg)](https://asciinema.org/a/400245)*** 

#### Version: [0.6](https://github.com/knassar702/scant3r/releases/tag/0.6)

![](.src/all.gif)

**Nokia** https://www.nokia.com/responsible-disclosure/
![](.src/nokia.gif)

**IBM** https://hackerone.com/ibm

![](.src/ibm.png)
