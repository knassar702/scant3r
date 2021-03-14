#!/usr/bin/env python3
from flask import Flask,request,jsonify,render_template
from glob import glob
from importlib import import_module
from yaml import safe_load

app = Flask(__name__)
conf = glob('modules/*/api.py')
al = dict()

for c,i in enumerate(conf):
    al[c] = i.split('/')[1]

class Server:
    def __init__(self,r,opts):
        self.http = r
        conf = safe_load(open('core/api/conf.yaml','r'))
        self.host = conf['host']
        self.port = conf['port']
        self.debug = conf['debug']
        self.opts = opts
    def index(self):
        return render_template('index.html',args=al)
    def scanapi(self,scanid):
        url = request.form.get('url',None)
        if url:
            if scanid in al.keys():
                try:
                    res = {'Results':[]}
                    m = import_module(f'modules.{al[scanid]}.api')
                    scan = m.main(url,self.opts,self.http)
                    if scan:
                        res['Results'] = scan
                    if len(res['Results']) > 0:
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
            return '<h4>add url parameter .!!</h4>',404
    def run(self):
        app.add_url_rule('/', view_func=self.index)
        app.add_url_rule('/scan/<int:scanid>',methods=['POST'],view_func=self.scanapi)
        app.run(host=self.host,port=self.port,debug=self.debug)

