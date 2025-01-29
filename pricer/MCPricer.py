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
            self.stock_sim_data = self.gbm.generate_paths(self.maturity,10000,100)
        return self.stock_sim_data
    
    def get_stock_sims_for_chart(self):
        percentiles = [99.9,99.5,99,90,75,50,25,10,1,0.5,0.01]
        stock_simulations = self.get_stock_sims()
        stock_percentiles = np.nanpercentile(stock_simulations['stock_prices'],percentiles,axis=0)
        opt_price = self.price_basic_option()
        res_sim = {}
        res_sim['time_axis'] = list(stock_simulations['time_axis'])
        res_sim['stock_percentiles'] = stock_percentiles.tolist()
        res_sim['percentiles'] = percentiles
        res_sim['opt_price'] = opt_price
       
        return res_sim

    def price_basic_option(self, stock_price = None, strike = None, maturity = None, volatility = None, risk_free_rate = None) -> float:
        T = self.maturity if maturity is None else maturity
        K = self.strike if strike is None else strike
        r = self.riskfree_rate if risk_free_rate is None else risk_free_rate
        if self.stock_sim_data is None:
            self.get_stock_sims()
        stock_sim_data = np.array(self.stock_sim_data["stock_prices"])
        nrow, ncol = stock_sim_data.shape
        if self.option_type == "call":
            terminal_payoffs = stock_sim_data[:,ncol-1] - K
            terminal_payoffs[terminal_payoffs < 0] = 0
            terminal_payoffs = terminal_payoffs * (1 if self.is_long else -1)
            return np.exp(-r*T) * np.mean(terminal_payoffs)
        elif self.option_type == "put":
            terminal_payoffs = K - stock_sim_data[:,ncol-1]
            terminal_payoffs[terminal_payoffs < 0] = 0
            terminal_payoffs = terminal_payoffs * (1 if self.is_long else -1)
            return np.exp(-r*T) * np.mean(terminal_payoffs)
        else:
            return None


