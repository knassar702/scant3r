## ScanT3r - Web Security Scanner 
<img src="https://i.ibb.co/fCtLQTz/received-2427790527459077.png" alt="ScanT3r Logo" border="0">
````

	   _____                ___________     
	  / ___/_________ _____/_  __/__  /_____
	  \__ \/ ___/ __ `/ __ \/ /   /_ </ ___/
	 ___/ / /__/ /_/ / / / / /  ___/ / /    
	/____/\___/\__,_/_/ /_/_/  /____/_/
	
	# Coded By : Khaled Nassar @knassar702

````
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

### Screen Shot :
   * ##### Nokia Website:
      * <img src="https://i.ibb.co/4N9mdtQ/nokai-sx.png" alt="nokia-xss" border="0"></a>

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
  -h, --help          |    show this help menu
  -u URL, --url=URL   |    Target URL (e.g."http://www.target.com/vuln.php?id=1")
  --data=DATA         |    Data string to be sent through POST (e.g. "id=1")
  --list=FILE         |    Get All Urls from List..
  --threads=THR       |    Max number of concurrent HTTP(s) requests (default 10)
  --timeout=time      |    Seconds to wait before timeout connection
  --cookies=COK       |    HTTP Cookie header value (e.g. "PHPSESSID=a8d127e..")
  --encode=1          |    How Many encode the payload (default 1)
````
### Example :

``` $ python3 scant3r -u 'http://localhost/dvwa/vulnerabilities/exec/' --data='ip=localhost&Submit=Submit' --cookies='PHPSESSID=safasf' ```
### Demo : <a href='http://youtube.com'> Video </a>
### Blog : <a href='http://knassar702.blogspot.com'> Blog </a>
##### Please send all your feedback and suggestions to: knassar702@gmail.com
