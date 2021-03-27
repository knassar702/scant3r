from flask import Flask,request


app = Flask(__name__)


@app.route('/',methods=['GET','POST'])
def index():
    r = request.get_json(silent=True)
    return f'{r}'


app.run()
