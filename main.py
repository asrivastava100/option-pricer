from pricer.BSPricer import BSPricer
from pricer.Portfolio import Portfolio
from pricer.GeometricBrownianMotion import GeometricBrownianMotion
from pricer.MCPricer import MCPricer

def main():
    #testing BSPricer and Portfolio classes
    c = BSPricer('call', 3/12, 100, 95, 0.5, 0.01,True)
    print(c.price_basic_option())
    print(c.get_delta())
    portfolio_1 = Portfolio(3/12, 100, 0.5, 0.01)
    portfolio_1.add_new_option('call', 95, True)
    print(portfolio_1.portfolio_premium())
    print(portfolio_1.portfolio_delta())
    portfolio_1.add_new_option('call', 95, True)
    print(portfolio_1.portfolio_premium())
    print(portfolio_1.portfolio_delta())
    #print(portfolio_1.multi_option_price_run())
    #testing GBM
    gbm = GeometricBrownianMotion(100,0.5,0.01)
    gbm.generate_paths(1,10,100)
    m = MCPricer("call",0.25,100,95,0.5,0.01,True)
    print("MC pricer:", m.price_basic_option())
    print("BS pricer:", c.price_basic_option())
    

if __name__=="__main__":
    main()