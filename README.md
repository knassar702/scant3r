<img src="https://i.ibb.co/fCtLQTz/received-2427790527459077.png" alt="ScanT3r Logo" border="0">
# ScanT3r - Web application Security Scanner

### Features:

* ##### Detect This Vulnerables
  * <h5>Remote Code Execution</h5>
    <ul><li>Linux</li></ul>
  * <h5>XSS Reflected</h5>
  * <h5>Template Injection</h5>
     <ul>
     <li> Jinja2 </li>
     <li> ERB </li>
     <li> Java </li>
     <li> Twig </li>
     <li> Freemarker </li>
     </ul>
  * <h5>SQl Injection </h5> 
* Support Post Request
* Bypass KingWaf
* Use Random ```user-agent``` in requests
* Change The Timeout
* Add Cookies
* Remote in all thing in your request like (```add custom user-agent and allow to redirect.. etc```)
* Support Scanning from List File
* how many Seconds sleeping after send one request
* Threading For Speeds
### Screen Shot :
   * ##### Nokia Website:
      * <img src="https://i.ibb.co/4N9mdtQ/nokai-sx.png" alt="nokia-xss" border="0"></a>

## Test ScanT3r
#### You can download dvwa or hacking-lab for test scant3r tool

#### OS Support :
- <h5> Linux</h5>
- <h5> Android</h5>
- <h5> Windows</h5>

## Install
### [Linux](https://wikipedia.org/wiki/Linux) [![alt tag](http://icons.iconarchive.com/icons/dakirby309/simply-styled/32/OS-Linux-icon.png)](https://fr.wikipedia.org/wiki/Linux)
* open your terminal 
* enter this command 
   ````
   $ git clone https://github.com/knassar702/scant3r 
   $ cd scant3r 
   $ python3 -m pip install -r requirements.txt
   ````
### Andoird <img src="https://img.icons8.com/clouds/100/000000/android-os.png">
* Download <a href='https://play.google.com/store/apps/details?id=com.termux&hl=en'>Termux App</a>
* open termux app
* enter this command
````bash
 $ pkg install python -y 
 $ pkg install git -y 
 $ git clone https://github.com/knassar702/scant3r
 $ cd scant3r 
 $ python3 -m pip install -r requirements.txt
````
### Windows <img src="https://img.icons8.com/color/48/000000/windows-10.png">
* Download <a href='https://www.python.org/downloads/windows/'>python3</a> and install it
* open your cmd
* enter this command 
````
$ python3 -m pip install -r requirements.txt
````

## Usage :
````
Options:
  -h, --help          |    Show help message and exit
  --version           |    Show program's version number and exit
  -u URL, --url=URL   |    Target URL (e.g."http://www.target.com/vuln.php?id=1")
  --data=DATA         |    Data string to be sent through POST (e.g. "id=1")
  --list=FILE         |    Get All Urls from List
  --threads           |    Max number of concurrent HTTP(s) requests (default 10)
  --timeout           |    Seconds to wait before timeout connection
  --proxy             |    Start The Connection with http(s) proxy
  --cookies           |    HTTP Cookie header value (e.g. "PHPSESSID=a8d127e..")
  --encode            |    How Many encode the payload (default 1)
  --allow-redirect    |    Allow the main redirect
  --verify            |    Enable HTTPS Cert
  --user-agent        |    add custom user-agent
  --sleep             |    Sent one request after some Seconds 
````
### Example :

``` $ python3 scant3r -u 'http://localhost/dvwa/vulnerabilities/exec/' --data='ip=localhost&Submit=Submit' --cookies='PHPSESSID=safasf' ```
