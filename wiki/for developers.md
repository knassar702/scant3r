Hello :D

this a quike describa about file & functions job

* **scant3r.py** - main file for run scant3r , start with import opts parser class and parse all options and add them to functions like http/moudles run
* **core/libs/all/** - scant3r functions folder
* **core/libs/all/data.py** - all parsing functions (cookies,requests,body,etc..)
* **core/libs/all/colors.py** - all colors
* **core/libs/all/args.py** - parsing args from user , this class works with two steps first load `conf/opts.yaml` file and get all main options of scant3r and after that it will start parsing command line args
* **core/libs/all/requester.py** - send http/s requests this module get all options from user (command line args) and save it in class vars , you can call it with your options without put them again
* **core/libs/all/module_loader.py** - load all users modules and run them in single thread
* **core/libs/all/logo.py** - read `conf/logo/*.txt` and replace `{colors}` with colors value from `core/libs/all/colors.py`
* **core/libs/all/show_msg.py** - this moudle for display the output of modules just add the name of output and request var , and add your info with more args in function after that show_msg will save the output in `log/{TARGET}/log.txt`
* **core/api/api.py** - the api of scant3r , the idea when scant3r api start will parse all modules files and try to get api.py file if the file there will give the module a id for scan


here about how to write your own scant3r module https://github.com/knassar702/scant3r/wiki/write-module-for-api
