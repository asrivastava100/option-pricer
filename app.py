from flask import Flask, send_file
from pricer import BSPricer

app = Flask(__name__,
            static_url_path='/web/static')

@app.route("/")
def hello_world():
    return send_file('web/static/index.html')

