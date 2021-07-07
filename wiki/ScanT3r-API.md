
### run
* Normal
```bash
$ python3 scant3r.py -a
```
you can connection options with API

```bash
$ python3 scant3r.py -a -p http://localhost:8080 -H 'Cookies: admin=True'
```

* Docker ![DOCKER](https://img.icons8.com/color/48/000000/docker.png)
```bash
$ docker build -t scant3r https://github.com/knassar702/scant3r.git
$ docker run --rm -d -p 6030:6030 --name scant3r -it scant3r
```
### API Configuration file
* `core/api/conf.yaml`

### API Endpoints
#### Scanning
   * Endpoint: /scan/{scanid}
   * Method: POST
   * parameter: `url`
#### Get output
   * Endpoint: /get/{scanid}
   * Method: GET

scant3r load all `api.py` files from `/modules/MODULE/api.py` , so you can call your module from api by id of your module (you can find all modules id in home page)

```bash
$ curl -X POST --data-urlencode "url=https://yourtarget.com/path?parameter=test" http://localhost:6030/scan/{scanid}
```

#### Example:
* XSS
```bash
$ curl -X POST --data-urlencode "url=http://testphp.vulnweb.com/search.php?test=query&searchFor=1&goButton=go"  http://0.0.0.0:6030/scan/0
{"Error":null}
```
get output
```bash
$ curl http://0.0.0.0:6030/get/0 -sk | jq

➜ khaled@ourpc  ~/myprojects/scant3r git:(master) ✗ curl http://0.0.0.0:6030/get/0 -sk| jq
[
  [
    {
      "Bug": "XSS",
      "method": "POST",
      "params": "test=query&searchFor=1\">ScanT3r<svg/onload=confirm(/ScanT3r/)>web\"&goButton=go",
      "url": "http://testphp.vulnweb.com/search.php"
    }
  ]
]

```