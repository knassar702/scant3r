hello , scant3r loads all options from `core/settings/opts.yaml` file
so add your options to opts.yaml file , like that


![opts screenshot](https://github.com/knassar702/scant3r/blob/master/.src/opts.png)

```yaml
myoption:
    - option: '-j'
    - type: 'string' # int > integer | false > this option doesn't require data
    - save_content: True | option value = True
    - help: "add custom option" # about option
    - default: '{}' # default value of option argument
# all options in class so to store your option in opts ,write what you want do with the argument
    - exec: 'self.myoption = opts.myoption'
```

### Why .?
if your module need more options , for example auth option 

```yaml
auth:
  - option: '-o'
  - type: string
  - save_content: True
  - help: add auth header
  - default: ''
  - exec: 'self.auth = extractHeaders(opts.auth)'
```


so let's describe this values

```
NAME:
   - option: '-o' # command line option name
   - type: string # your option value need to be string or integer
   - save_content: # your option require a values | true = -o hello  > NAME = hello | false = -o hello > NAME = hello
   - help: 'HELP' # option help message
   - default: 'TEST' # Default option value
   - exec: 'self.NAME = opts.NAME' # also you can add this values to functions 
```


```$ ./scant3r.py -h 

Options:
  -h | show help menu and exit
  -o | add auth header
   ... | ...

```

```

$ ./scant3r.py -o 'man: LOL' -m test

   ____              __  ____
  / __/______ ____  / /_|_  /____
 _\ \/ __/ _ `/ _ \/ __//_ </ __/
/___/\__/\_,_/_//_/\__/____/_/


[!] Coded by : Khaled Nassar @knassar702
[!] Version : 0.7#Beta
    	
Modules Loaded :> 1
Hello , for testing 

Your Options:  {'urls': ['http://google.com'],'auth': {'man': 'LOL'},.....]
```