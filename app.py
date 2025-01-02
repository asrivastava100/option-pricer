from flask import Flask, request, jsonify
from pricer.BSPricer import BSPricer
from pricer.Portfolio import Portfolio

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
    is_long       = request.args.get("isLong") == "True"
    bs = BSPricer(option_type, maturity, stock_price, strike, volatility, riskfree_rate,is_long)
    return str(bs.price_basic_option())

@app.route("/api/priceMultipleOptions")
def price_multiple_option():
    option_type   = request.args.get("optionType")
    maturity      = float(request.args.get("maturity"))
    stock_price   = float(request.args.get("stockPrice"))
    strike        = float(request.args.get("strike"))
    volatility    = float(request.args.get("volatility"))
    riskfree_rate = float(request.args.get("riskFreeRate"))
    is_long       = request.args.get("isLong") == "True"
    bs = BSPricer(option_type, maturity, stock_price, strike, volatility, riskfree_rate,is_long)
    return jsonify(bs.multi_option_price_run())

@app.route("/api/pricePortfolio")
def price_portfolio():
    maturity      = float(request.form["maturity"])
    stock_price   = float(request.form["stockPrice"])
    volatility    = float(request.form["volatility"])
    riskfree_rate = float(request.form["riskFreeRate"])
    options       = request.form["options"]
    option_portfolio = Portfolio(maturity, stock_price, volatility, riskfree_rate)
    for option in options:
        option_portfolio.add_new_option(option["type"],float(option['strike']),option['is_long']== "True")
    return jsonify(option_portfolio.multi_option_price_run())


