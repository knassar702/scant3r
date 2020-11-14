#!/usr/bin/env python3
from flask import Flask,request,jsonify
from vuln import Xss,Sqli,RCE,CRLF,SSTI

def xss(url):
    res = []
    get = Xss.Get(url)
    post = Xss.Post(url)
    put = Xss.Put(url)
    if get:
        res.append(get)
    if post:
        res.append(post)
    if put:
        res.append(put)
    if len(res) > 0:
        return res
def rce(url):
    res = []
    get = RCE.Get(url)
    post = RCE.Post(url)
    put = RCE.Put(url)
    if get:
        res.append(get)
    if post:
        res.append(post)
    if put:
        res.append(put)
    if len(res) > 0:
        return res
def sqli(url):
    res = []
    get = Sqli.Get(url)
    post = Sqli.Post(url)
    put = Sqli.Put(url)
    if get:
        res.append(get)
    if post:
        res.append(post)
    if put:
        res.append(put)
    if len(res) > 0:
        return res
def ssti(url):
    res = []
    get = SSTI.Get(url)
    post = SSTI.Post(url)
    put = SSTI.Put(url)
    if get:
        res.append(get)
    if post:
        res.append(post)
    if put:
        res.append(put)
    if len(res) > 0:
        return res
def crlf(url):
    res = []
    get = SSTI.Get(url)
    if get:
        res.append(get)
    if len(res) > 0:
        return res
app = Flask(__name__)
@app.route('/')
def index():
    return '''
<!DOCTYPE html>
<html>
<style>
table, th, td {
  border: 1px solid black;
  border-collapse: collapse;
}
th, td {
  padding: 5px;
  text-align: left;
}
</style>
</head>
<body>

<h2> <a href='https://github.com/knassar702/scant3r'>ScanT3r</a> - API </h2>

<p>http://localhost:6040/scan/{SCANNER_ID}?url={TAGET}</p>

example : <h5>$ curl 'http://localhost:6040/scan/1?url=http://testphp.vulnweb.com/search.php?test=query%26searchFor=1%26goButton=go'</h5>

<table style="width:70%">
  <tr>
    <th>ID</th>
    <th>Scanner</th> 
  </tr>
  <tr>
    <td>1</td>
    <td>XSS</td>
  </tr>
  <tr>
    <td>2</td>
    <td>SQLI</td>
  </tr>
  <tr>
    <td>3</td>
    <td>RCE</td>
  </tr>
  <tr>
    <td>4</td>
    <td>SSTI</td>
  </tr>
  <tr>
    <td>5</td>
    <td>CRLF</td>
  </tr>
</table>

</body>
</html>

    '''

@app.route('/scan/<int:scanid>')
def scanapi(scanid):
    url = request.args.get('url',None)
    if url:
        if scanid in [1,2,3,4,5]:
            try:
                res = {'Bugs':[]}
                if scanid == 1:
                    scan = xss(url)
                elif scanid == 2:
                    scan = sqli(url)
                elif scanid == 3:
                    scan = rce(url)
                elif scanid == 4:
                    scan = ssti(url)
                elif scanid == 5:
                    scan = crlf(url)
                if scan:
                    res['Bugs'] = scan
                if len(res['Bugs']) > 0:
                    return jsonify(res)
                else:
                    return jsonify('null')
            except IndexError:
                return jsonify({'URL Processing Error':True})
            except Exception as e:
                return jsonify({'Error':f'{e}'})
        else:
            return jsonify({'Scanid':'404'})
    else:
        return '<h4>add url parameter .!!</h4>'
