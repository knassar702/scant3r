#!/usr/bin/env python3
from flask import Flask,abort,request,jsonify,render_template
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flasgger import Swagger, swag_from
from werkzeug.security import generate_password_hash
from glob import glob
from importlib import import_module
from yaml import safe_load
from threading import Thread
from core.libs import Http
import sys,os

app = Flask(__name__)
app.config['SWAGGER'] = {
    'title': 'ScanT3r API',
    'uiversion': 3,
    "specs_route": "/"
}
class Server:
    def __init__(self,opts):
        conf = safe_load(open('conf/api.yaml','r'))
        self.host = conf['host']
        self.port = conf['port']
        self.check_token = conf['check_token']
        self.debug = conf['debug']
        self.opts = opts
        self.output = dict()
        if conf['token'] == '$RANDOM$':
            try:
                conf['token'] = generate_password_hash(os.urandom(30).decode('utf-16')).lstrip('pbkdf2:sha256:')
            except UnicodeDecodeError:
                self.restart()
        if conf['check_token'] == False:
            print(f"""
======================
|YOUR RANDOM API TOKEN: {conf['token']}
======================
            """)
        app.config['SECRET_KEY'] = conf['token']
        limiter = Limiter(
        app,
        key_func=get_remote_address,
        default_limits=conf['limits']
        )
    def restart(self):
        exe = sys.executable
        user_args = sys.argv
        if '-n' in user_args or '--no-logo' in user_args:
            pass
        else:
            user_args.append('-n')
        os.execl(ex, ex, * sys.argv)
        return
    def clearme(self):
        self.output = dict()
        return {'Done':True}
    def get_m(self):
        conf = glob('modules/*/api.py')
        al = dict()
        for c,i in enumerate(conf):
            al[c] = i.split('/')[1]
        return al
    def save_output(self,func,scanid,copts):
        v = func.main(copts,Http(copts))
        scanid = str(scanid)
        if v:
            self.output[scanid].append(v)
    def index(self):
        return swag
        #return render_template('index.html',args=self.get_m())
    def getit(self):
        if self.check_token != True:
            if 'token' not in req_params.keys():
                return {
                    "Error":"token parameter missing"
                }
        else:
            if 'token' in req_params.keys():
                if req_params['token'] != app.config['SECRET_KEY']:
                    return {
                        "Error":"Auth Error"
                    }
        cc = {}
        for i,v in self.output.items():
            if self.output[i]:
                if v:
                    c = self.get_m()[int(i)]
                    cc[c] = v
        return jsonify(cc)
    def getme(self,mid):
        if self.check_token != True:
            if 'token' not in req_params.keys():
                return {
                    "Error":"token parameter missing"
                }
        else:
            if 'token' in req_params.keys():
                if req_params['token'] != app.config['SECRET_KEY']:
                    return {
                        "Error":"Auth Error"
                    }
        try:
            c = []
            for v in self.output[str(mid)]:
                c.append(v)
            return jsonify(c)
        except Exception as e:
            return {'Error':f'Not Found'},404
    def orgparams(self,d):
        v = self.opts.copy()
        for i,o in d.items():
            if o:
                v[i] = o
        return v
    def scanapi(self,scanid):
        req_params = request.get_json(force=True)
        self.url = None
        if 'url' in req_params.keys():
            self.url = req_params['url']
        if self.check_token != True:
            if 'token' not in req_params.keys():
                return {
                    "Error":"token parameter missing"
                }
        else:
            if 'token' in req_params.keys():
                if req_params['token'] != app.config['SECRET_KEY']:
                    return {
                        "Error":"Auth Error"
                    }
        if 'url' in req_params.keys():
            self.url = req_params['url']

        if self.url:
            try:
                self.output[str(scanid)]
            except:
                self.output[str(scanid)] = list()
            copts = self.orgparams(request.get_json(force=True))
            if scanid in self.get_m().keys():
                try:
                    res = {'Results':[]}
                    try:
                        m = import_module(f'modules.{self.get_m()[scanid]}.api')
                    except Exception as e:
                        return jsonify({'Error':e}),500
                    p1 = Thread(target=self.save_output,args=(m,scanid,copts,))
                    p1.daemon = True
                    p1.start()
                    return {'Start':True}

                except Exception as e:
                    return jsonify({'Error':f'{e}'})
            else:
                return jsonify({'Error':'Scanid not found'})
        else:
            return {'Error':'url paremter is required'},404
    def run(self):
        app.add_url_rule('/', view_func=self.index)
        app.add_url_rule('/scan/<int:scanid>',methods=['POST'],view_func=self.scanapi)
        app.add_url_rule('/scan/',view_func=self.getit)
        app.add_url_rule('/restart',view_func=self.restart)
        app.add_url_rule('/clear',view_func=self.clearme)
        app.add_url_rule('/scan/<int:mid>',view_func=self.getme)
        app.run(host=self.host,port=self.port,debug=self.debug)
