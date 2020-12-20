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
    return render_template('index.html')

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
