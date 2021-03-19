#!/usr/bin/env python3
from flask import Flask,abort,request,jsonify,render_template
from glob import glob
from importlib import import_module
from yaml import safe_load
from threading import Thread

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
        self.output = dict()
    def save_output(self,func,scanid):
        v = func.main(self.op,self.http)
        scanid = str(scanid)
        self.output[scanid].append(v)
    def index(self):
        return render_template('index.html',args=al)
    def getit(self):
        return jsonify(self.output)
    def getme(self,mid):
        try:
            return jsonify(self.output[str(mid)])
        except Exception as e:
            return {'Error':f'Not Found'},404
    def scanapi(self,scanid):
        self.url = request.form.get('url',None)

        if self.url:
            try:
                self.output[str(scanid)]
            except:
                self.output[str(scanid)] = list()
            if scanid in al.keys():
                try:
                    res = {'Results':[]}
                    self.op = self.opts.copy()
                    self.op['url'] = self.url
                    try:
                        m = import_module(f'modules.{al[scanid]}.api')
                    except Exception as e:
                        return jsonify({'Error':e})
                    p1 = Thread(target=self.save_output,args=(m,scanid,))
                    p1.daemon = True
                    p1.start()
                    return {
                            'Error':None
                            }
                except Exception as e:
                    return jsonify({'Error':f'{e}'})
            else:
                return jsonify({'Scanid':'404'})
        else:
            return '<h4>add url parameter .!!</h4>',404
    def run(self):
        app.add_url_rule('/', view_func=self.index)
        app.add_url_rule('/scan/<int:scanid>',methods=['POST'],view_func=self.scanapi)
        app.add_url_rule('/get',view_func=self.getit)
        app.add_url_rule('/get/<int:mid>',view_func=self.getme)
        app.run(host=self.host,port=self.port,debug=self.debug)

