from BSPricer import BSPricer
from Portfolio import Portfolio

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

if __name__=="__main__":
    main()