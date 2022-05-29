
<h3 align="center">
  <img src="https://user-images.githubusercontent.com/45688522/170871350-80113c02-5733-4d04-9f09-c33bef80c2bf.png" width="600px">
</h3>



<h1 align="center">
  <br>
  <br>
  ScanT3r <br><h4 align="center">Save your scripting time</h4>
  <br>  
</h1>

<p align="center">
  <a href="https://github.com//scant3r/releases">
    <img src="https://img.shields.io/github/release/knassar702/scant3r.svg">
  </a>
  <a href="https://github.com/knassar702/scant3r/issues?q=is%3Aissue+is%3Aclosed">
      <img src="https://img.shields.io/github/issues-closed-raw/knassar702/scant3r?color=dark-green&label=issues%20fixed">
  </a>
  <a href="https://img.shields.io/github/stars/knassar702/scant3r">
      <img src="https://img.shields.io/github/stars/knassar702/scant3r">
  </a>
  <a href="https://img.shields.io/github/forks/knassar702/scant3r">
      <img src="https://img.shields.io/github/forks/knassar702/scant3r">
  </a>
  <a href="https://img.shields.io/github/issues/knassar702/scant3r">
      <img src="https://img.shields.io/github/issues/knassar702/scant3r">
  </a>
  <a href="https://img.shields.io/github/license/knassar702/scant3r">
      <img src="https://img.shields.io/github/license/knassar702/scant3r">
  </a>
</p>

***

### What's this?
this is a module-based web automation tool that I made for saving my scripting
time by providing some utilises that everybody needs in his automation script
instead of focusing on ( logger, parsers, output function , cmd args, multi-threading) ,
just write the logic of your scanning idea with scant3r utils without caring
about these things, you can find callback/parsing/logging utils and output functions, Also we will adding Restful API soon <br>
what if you need to add new Command option to scant3r for your script? <br>
easy without writing any code just open `conf/opts.yaml` file and you will find all options of scant3r so you can change and add what you want;D


```yaml
# conf/opts.yaml
exit_after:
  - option: 
    - '-e' # SHORT
    - "--exit-after" # LONG
  - type: int # TYPE OF VALUE
  - default: 500 # DEFAULT
  - save_content: true # SHOUD I SAVE THE CONTENT OF THIS OPTION ?
  - help: "Exit after get this number of errors" # HELP MESSAGE
  - exec: "dict_args['exit_after'] = int(value)" # HOW TO SAVE IT IN OPTS DICT
```

### why should I use it ?
the short answer is to save your time, you as a security guy you don't need to
learn more about " how to write a perfect CLI script " you just need to
understand the logic of your script <br> if you need to write something like SSRF
CVE scanner, instead of searching "How can I call interact.sh", "how to fix this
code issue", "how can I parse this' <br> and after getting the answer you will get
some cool errors in your code and you will find yourself needing more time to
search and fix these bugs
![speedrun](https://c.tenor.com/xRKRAjXmEVcAAAAd/sweaty-sweaty-speedrunner.gif)

you as a security guy this is a waste of time for you, so this project will help to
save more and more, just take a look at the examples modules and read the
official documentation (unavailable yet), or just open an issue with a
Feature request and we will write your script by our hands

### Modules

this the modules we providing for our community for you need new module open an issue with `Feature request
` template 

| module         | Short description                                           |
| :------------- | :-------------                                               |
| **req_callback**     | Finds Out-of-band Resources parameters |
| **ssti**       | Finds Server-side Template injection                                         |
| **firebase**   | checks for public firebase databases (write/read) permission  |

#### Requirements
* python >= 3.6
* pip
* Git

#### install
* Unix & MS-DOS

```bash
$ git clone https://github.com/knassar702/scant3r
$ cd scant3r
$ python3 setup.py install
$ python3 -m scant3r --help
```


##### Options

## TODO-Features
* [ ] Restful API
* [ ] Command line Modules ( with yaml file )
* [ ] Custom scanning map
* [ ] Selenium Modules

## Acknowledgments
* [@knassar702](https://github.com/knassar702)
* [@MariusVinaschi](https://github.com/MariusVinaschi) (big thanks)
* [@0xflotus](https://github.com/0xflotus)
* [@pdelteil](https://github.com/pdelteil)
* [@oppsec](https://github.com/oppsec)


#### Join us 
if you wanna to join us a python developer you can send an email to the owner of this project ( knassar702@gmail.com )

## License
* [GPL 3v](https://github.com/knassar702/scant3r/blob/master/LICENSE)


### Stars Rate
![stars](https://starchart.cc/knassar702/scant3r.svg)

***

## Media
some demo gifs from the old versions

* LorSrf
![](.src/output.gif)

#### Version: [0.6](https://github.com/knassar702/scant3r/releases/tag/0.6)

![](.src/all.gif)

**Nokia** https://www.nokia.com/responsible-disclosure/
![](.src/nokia.gif)

**IBM** https://hackerone.com/ibm

![](.src/ibm.png)
