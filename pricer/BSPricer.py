from statistics import NormalDist
import math

class BSPricer:
    def __init__(self, 
                 option_type:str, 
                 maturity:float, 
                 stock_price:float, 
                 strike:float, 
                 volatility:float, 
                 riskfree_rate:float,
                 is_long:bool) -> None:
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
        self.is_long = is_long
        self.sign = 1 if self.is_long else -1

    def price_basic_option(self, stock_price:float = None, strike:float = None, maturity:float = None, volatility:float = None, risk_free_rate:float = None) -> float:
        """
        Returns the call / put price. 
        S = Stock price
        K = Strike
        T = time to maturity
        Sigma = volatility
        r = risk free rate
        Call price = N(d1)*S - N(d2)*K*exp(-r*T)
        Put price = -N(-d1)*S + N(-d2)*K*exp(-r*T)
        where d1 = (1/(sigma * sqrt(T))) * (log(S/K) + (r+0.5*sigma^2)*T)
        d2 = d1 - sigma * sqrt(T)
        N(d) is the standard normal cdf
        """
        sigma = self.volatility if volatility is None else volatility
        T = self.maturity if maturity is None else maturity
        K = self.strike if strike is None else strike
        S = self.stock_price if stock_price is None else stock_price
        r = self.riskfree_rate if risk_free_rate is None else risk_free_rate
        d1 = (1/(sigma * math.sqrt(T))) * (math.log(S/K) + (r+0.5*sigma**2)*T)
        d2 = d1 - sigma * math.sqrt(T)
        if self.option_type == "call":
            return self.sign * (NormalDist().cdf(d1)*S - NormalDist().cdf(d2)*K*math.exp(-r*T)) 
        elif self.option_type == "put":
            return self.sign * (-NormalDist().cdf(-d1)*S + NormalDist().cdf(-d2)*K*math.exp(-r*T))
        else:
            return None
    
    def get_delta(self, stock_price:float = None) -> float:
        """
        Returns the option delta
        S = Stock price
        K = Strike
        T = time to maturity
        Sigma = volatility
        r = risk free rate
        delta call = N(d1)
        delta put = N(d1) - 1
        where d1 = (1/(sigma * sqrt(T))) * (log(S/K) + (r+0.5*sigma^2)*T)
        """
        sigma = self.volatility
        T = self.maturity
        K = self.strike
        S = stock_price if stock_price is not None else self.stock_price
        r = self.riskfree_rate
        d1 = (1/(sigma * math.sqrt(T))) * (math.log(S/K) + (r+0.5*sigma**2)*T)
        if self.option_type == "call":
            return self.sign * NormalDist().cdf(d1)
        elif self.option_type == "put":
            return self.sign * (NormalDist().cdf(d1) -1)
        else:
            return None

    def multi_option_price_run(self):
        """
        Returns options prices for different stock prices. Also returns terminal payoffs.
        Range of stock price = (0.5 * stock_price, 1.5 * stock_price)
        """
        lower = int(0.5 * self.stock_price) + 1
        upper = int(1.5 * self.stock_price) + 1
        stock_prices = [i for i in range(lower,upper)]
        option_prices = [self.price_basic_option(price) for price in stock_prices]
        terminal_values = [self.sign * max(price - self.strike,0) if self.option_type == "call" else self.sign * max(self.strike - price,0) for price in stock_prices]
        deltas = [self.get_delta(price) for price in stock_prices]
        current_option_price_idx = int(len(stock_prices) / 2) - 1
        current_option_price = option_prices[current_option_price_idx]
        return {"stock_prices":stock_prices, 
                "option_prices":option_prices, 
                "terminal_values":terminal_values,
                "deltas":deltas,
                "current_option_price":current_option_price}
        
    
        

    