from statistics import NormalDist
import math

class BSPricer:
    def __init__(self, 
                 option_type:str, 
                 maturity:float, 
                 stock_price:float, 
                 strike:float, 
                 volatility:float, 
                 riskfree_rate:float) -> None:
        """
        option_type: 'call' or 'put'
        maturity, stock_price, volatility: must be positive floats
        """    
        self.option_type = option_type
        self.maturity = maturity
        self.stock_price = stock_price
        self.strike = strike
        self.volatility = volatility
        self.riskfree_rate = riskfree_rate

    def price_call(self) -> float:
        """
        Returns the call / put price. 
        S = Stock price
        K = Strike
        T = time to maturity
        Sigma = volatility
        r = risk free rate
        Call price = N(d1)*S - N(d2)*K*exp(-r*T)
        where d1 = (1/(sigma * sqrt(T))) * (log(S/K) + (r+0.5*sigma^2)*T)
        d2 = d1 - sigma * sqrt(T)
        N(d) is the standard normal cdf
        """
        sigma = self.volatility
        T = self.maturity
        K = self.strike
        S = self.stock_price
        r = self.riskfree_rate
        d1 = (1/(sigma * math.sqrt(T))) * (math.log(S/K) + (r+0.5*sigma**2)*T)
        d2 = d1 - sigma * math.sqrt(T)
        price = NormalDist.cdf(d1)*S - NormalDist.cdf(d2)*K*math.exp(-r*T)
        return price

