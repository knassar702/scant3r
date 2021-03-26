#!/usr/bin/env python3
from flask import Flask,abort,request,jsonify,render_template
from glob import glob
from importlib import import_module
from yaml import safe_load
from threading import Thread
import sys,os

app = Flask(__name__)

class Server:
    def __init__(self,r,opts):
        self.http = r
        conf = safe_load(open('core/api/conf.yaml','r'))
        self.host = conf['host']
        self.port = conf['port']
        self.debug = conf['debug']
        self.opts = opts
        self.output = dict()
    def restart(self):
        python = sys.executable
        os.execl(python, python, * sys.argv)
        curdir = os.getcwd()
    def clearme(self):
        self.output = dict()
        return {'Done':True}
    def get_m(self):
        conf = glob('modules/*/api.py')
        al = dict()
        for c,i in enumerate(conf):
            al[c] = i.split('/')[1]
        return al
    def save_output(self,func,scanid):
        v = func.main(self.op,self.http)
        scanid = str(scanid)
        if len(v) > 0:
            self.output[scanid].append(v)
    def index(self):
        return render_template('index.html',args=self.get_m())
    def getit(self):
        cc = list()
        for i,v in self.output.items():
            if self.output[i]:
                cc.append(self.output)
        return jsonify(cc)
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
            if scanid in self.get_m().keys():
                try:
                    res = {'Results':[]}
                    self.op = self.opts.copy()
                    self.op['url'] = self.url
                    try:
                        m = import_module(f'modules.{self.get_m()[scanid]}.api')
                    except Exception as e:
                        return jsonify({'Error':e}),500
                    p1 = Thread(target=self.save_output,args=(m,scanid,))
                    p1.daemon = True
                    p1.start()
                    return {'Start':True}

                except Exception as e:
                    return jsonify({'Error':f'{e}'})
            else:
                return jsonify({'Scanid':'404'})
        else:
            return {'Error':'url paremter is required'},404
    def run(self):
        app.add_url_rule('/', view_func=self.index)
        app.add_url_rule('/scan/<int:scanid>',methods=['POST'],view_func=self.scanapi)
        app.add_url_rule('/get/',view_func=self.getit)
        app.add_url_rule('/get',view_func=self.getit)
        app.add_url_rule('/restart',view_func=self.restart)
        app.add_url_rule('/clear',view_func=self.clearme)
        app.add_url_rule('/get/<int:mid>',view_func=self.getme)
        app.run(host=self.host,port=self.port,debug=self.debug)
