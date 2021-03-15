# Scant3r - web application vulnerability scanner

**Why would you use Scant3r?**

scant3r will help you to write your own python script faster , you don't need to configure http/threads/errors/options/etc... , just by writing main function in your script , you can run it in your terminal or access your script from api :D


### Modules

| Module              | Description                   |
| :-------------    | :-------------                |
| **lorsrf** | Bruteforcing on Hidden parameters to find SSRF vulnerability |
| **paths** | Check for custom paths|
| **xss** | xss scanner|
| **injheaders** | inject blind xss and custom payloads in custom headers (headers.yaml&payload.yaml)
| **reflect** | find reflected parameters 

**If you want to write your own module**
* https://github.com/knassar702/scant3r/wiki/writing-your-own-scant3r-module

***
## Installation

### Linux ![Linux](http://icons.iconarchive.com/icons/dakirby309/simply-styled/32/OS-Linux-icon.png)

```bash
$ git clone https://github.com/knassar702/scant3r
$ cd scant3r
$ pip3 install -r requirements.txt
$ ./scant3r.py -h
```

#### Update to latest version:
```bash
$ cd scant3r
$ git pull
```
### Usage
* https://github.com/knassar702/scant3r/wiki/Usage

### ScanT3r Modules
* https://github.com/knassar702/scant3r/wiki/ScanT3r-Modules

### writing your own scant3r module
* https://github.com/knassar702/scant3r/wiki/writing-your-own-scant3r-module

### how to find hidden SSRF Parameters by using scant3r
* https://github.com/knassar702/scant3r/wiki/how-to-find-hidden-SSRF-Parameters-by-using-scant3r

### How to Find sensitive files by using ScanT3r
* https://github.com/knassar702/scant3r/wiki/How-to-Find-sensitive-files-by-using-ScanT3r

### ScanT3r API
* https://github.com/knassar702/scant3r/wiki/ScanT3r-API


### Screenshot 

# Version: [0.6](https://github.com/knassar702/scant3r/releases/tag/0.6)

![](.src/all.gif)

**Nokia** https://www.nokia.com/responsible-disclosure/
![](.src/nokia.gif)

**IBM** https://hackerone.com/ibm

![](.src/ibm.png)

**Blind SSRF Parameters (lorsrf)**
![](https://raw.githubusercontent.com/knassar702/scant3r/master/images/ssrf.gif)
