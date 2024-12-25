from flask import Flask, request, render_template
from pricer.BSPricer import BSPricer

app = Flask(__name__)

app.debug = True
@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route("/api/priceCall")
def priceCall():
    option_type   = request.args.get("optionType")
    maturity      = float(request.args.get("maturity"))
    stock_price   = float(request.args.get("stockPrice"))
    strike        = float(request.args.get("strike"))
    volatility    = float(request.args.get("volatility"))
    riskfree_rate = float(request.args.get("riskFreeRate"))
    bs = BSPricer(option_type, maturity, stock_price, strike, volatility, riskfree_rate)
    return str(bs.price_call())


