from pricer.BSPricer import BSPricer
from pricer.Portfolio import Portfolio
import pytest

def test_call_price():
    c = BSPricer('call', 0.25, 100, 95, 0.2, 0.03, True)
    assert c.price_basic_option() == pytest.approx(7.378954534893353)

def test_portfolio_straddle():
    p = Portfolio(0.25,100,0.2,0.03)
    p.add_new_option("call",95,True)
    p.add_new_option("put",95,True)
    res_obj = p.multi_option_price_run()
    prices = res_obj["current_option_price"]
    assert prices[0] == pytest.approx(7.378954534893353) and prices[1] == pytest.approx(1.6691197427114908)

def test_portfolio_bear_spread():
    p = Portfolio(0.25,100,0.2,0.03)
    p.add_new_option("put",95,True)
    p.add_new_option("put",90,False)
    res_obj = p.multi_option_price_run()
    prices = res_obj["current_option_price"]
    assert prices[0] == pytest.approx(1.6691197427114908) and prices[1] == pytest.approx(-0.6121949825582611)

        