logos folder
```
core/settings/logo/
├── logo
│   ├── 1.txt
│   └── 2.txt
```

```
$ cat 1.txt

{red}
   ____              __  ____
  / __/______ ____  / /_|_  /____
{yellow} _\ \/ __/ _ `/ _ \/ __//_ </ __/
{green}/___/\__/\_,_/_//_/\__/____/_/{rest}

{info} Coded by: Khaled Nassar @knassar702
{info} Version: 0.7#Beta
```
all colors list
```
$ python3
Python 3.8.5 (default, Jan 27 2021, 15:41:15) 
[GCC 9.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from core.libs import dump_colors
>>> dump_colors()
{'red': '\x1b[31m', 'rest': '\x1b[0m', 'black': '\x1b[30m', 'green': '\x1b[32m', 'yellow': '\x1b[33m', 'blue': '\x1b[34m', 'magenta': '\x1b[35m', 'cyan': '\x1b[36m', 'white': '\x1b[37m', 'bblack': '\x1b[30;1m', 'bred': '\x1b[31;1m', 'bgreen': '\x1b[32;1m', 'byellow': '\x1b[33;1m', 'bblue': '\x1b[34;1m', 'bmagenta': '\x1b[35;1m', 'bcyan': '\x1b[36;1m', 'bwhite': '\x1b[37;1m', 'Bblack': '\x1b[40m', 'Bred': '\x1b[41m', 'Bgreen': '\x1b[42m', 'Byellow': '\x1b[43m', 'Bblue': '\x1b[44m', 'Bcyan': '\x1b[46m', 'Bwhite': '\x1b[47m', 'BBblack': '\x1b[40;1m', 'BBred': '\x1b[41;1m', 'BBgreen': '\x1b[42;1m', 'BByellow': '\x1b[43;1m', 'BBblue': '\x1b[44;1m', 'BBmagenta': '\x1b[45;1m', 'BBcyan': '\x1b[46;1m', 'BBwhite': '\x1b[47;1m', 'good': '\x1b[33m[\x1b[0m\x1b[32m+\x1b[0m\x1b[33m]\x1b[0m', 'bad': '\x1b[33m[\x1b[0m\x1b[31m-\x1b[0m\x1b[33m]\x1b[0m', 'info': '\x1b[33m[\x1b[33m!\x1b[0m\x1b[33m]\x1b[0m'}
>>>
>>>
>>>
>>> for color,value in dump_colors().items():
...     print(f'{color}: {value}')

```

### add you logo
```
knassar702@OurPc:~/myproject/scant3r ☭ $ core/settings/logo/3.txt
knassar702@OurPc:~/myproject/scant3r ☭ $ figlet ScaNT3r > 3.txt
knassar702@OurPc:~/myproject/scant3r ☭ $ mv 3.txt core/settings/logo/3.txt
knassar702@OurPc:~/myproject/scant3r ☭ $  cat core/settings/logo/3.txt

 ____            _   _ _____ _____      
/ ___|  ___ __ _| \ | |_   _|___ / _ __ 
\___ \ / __/ _` |  \| | | |   |_ \| '__|
 ___) | (_| (_| | |\  | | |  ___) | |   
|____/ \___\__,_|_| \_| |_| |____/|_|  


knassar702@OurPc:~/myproject/scant3r ☭ $ # add your colors with {{}} (eg: {{red}})

 ____            _   _ _____ _____      
/{red} ___|  ___ __ _| \ | |_   _|___ / _ __ 
\___ \ / __/ _` |  {cyan}\| | | |   |_ \| '__|
 ___) | (_| (_| | |\  | | |  ___) | |   
|____/ \___\__,_|_| \_| |_| |____/|_| 
{info} Hello world
```
* save it and run :D
