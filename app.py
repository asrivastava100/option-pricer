from flask import Flask, request, jsonify
from pricer.BSPricer import BSPricer

app = Flask(__name__, static_folder="web", static_url_path="")

app.debug = True
@app.route("/")
def hello_world():
    return app.send_static_file('index.html')

@app.route("/api/priceBasicOption")
def price_basic_option():
    option_type   = request.args.get("optionType")
    maturity      = float(request.args.get("maturity"))
    stock_price   = float(request.args.get("stockPrice"))
    strike        = float(request.args.get("strike"))
    volatility    = float(request.args.get("volatility"))
    riskfree_rate = float(request.args.get("riskFreeRate"))
    bs = BSPricer(option_type, maturity, stock_price, strike, volatility, riskfree_rate)
    return str(bs.price_basic_option())

@app.route("/api/priceMultipleOptions")
def price_multiple_option():
    option_type   = request.args.get("optionType")
    maturity      = float(request.args.get("maturity"))
    stock_price   = float(request.args.get("stockPrice"))
    strike        = float(request.args.get("strike"))
    volatility    = float(request.args.get("volatility"))
    riskfree_rate = float(request.args.get("riskFreeRate"))
    bs = BSPricer(option_type, maturity, stock_price, strike, volatility, riskfree_rate)
    return jsonify(bs.multi_option_price_run())


