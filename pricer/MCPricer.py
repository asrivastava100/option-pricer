from pricer.GeometricBrownianMotion import GeometricBrownianMotion
import numpy as np

class MCPricer:
    def __init__(self, 
                 option_type:str, 
                 maturity:float, 
                 stock_price:float, 
                 strike:float, 
                 volatility:float, 
                 riskfree_rate:float,
                 is_long:bool) -> None:
        self.option_type = option_type
        self.maturity = maturity
        self.stock_price = stock_price
        self.strike = strike
        self.volatility = volatility
        self.riskfree_rate = riskfree_rate
        self.is_long = is_long
        self.sign = 1 if self.is_long else -1
        self.stock_sim_data = None
        self.gbm = GeometricBrownianMotion(self.stock_price,self.volatility,self.riskfree_rate)
        
    def get_stock_sims(self):
        if self.stock_sim_data is None:
            self.stock_sim_data = self.gbm.generate_paths(self.maturity,100,100)
        return self.stock_sim_data
    
    def get_stock_sims_for_chart(self):
        stock_simulations = self.get_stock_sims()
        res_sim = {}
        res_sim['stock_prices'] = list(stock_simulations['stock_prices'])
        res_sim['time_axis'] = list(stock_simulations['time_axis'])
        
        return res_sim

    def price_basic_option(self, stock_price = None, strike = None, maturity = None, volatility = None, risk_free_rate = None) -> float:
        sigma = self.volatility if volatility is None else volatility
        T = self.maturity if maturity is None else maturity
        K = self.strike if strike is None else strike
        S = self.stock_price if stock_price is None else stock_price
        r = self.riskfree_rate if risk_free_rate is None else risk_free_rate
        if self.stock_sim_data is None:
            self.get_stock_sims()
            nrow, ncol = self.stock_sim_data["stock_prices"].shape
        if self.option_type == "call":
            terminal_payoffs = self.stock_sim_data["stock_prices"][:,ncol-1] - K
            terminal_payoffs[terminal_payoffs < 0] = 0
            return np.exp(-r*T) * np.mean(terminal_payoffs)
        elif self.option_type == "put":
            terminal_payoffs = K - self.stock_sim_data["stock_prices"][:,ncol-1]
            terminal_payoffs[terminal_payoffs < 0] = 0
            return np.exp(-r*T) * np.mean(terminal_payoffs)
        else:
            return None


