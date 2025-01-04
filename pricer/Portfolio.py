from pricer.BSPricer import BSPricer

class Portfolio:
    def __init__(self,
                 maturity:float, 
                 stock_price:float,  
                 volatility:float,
                 riskfree_rate:float) -> None:
        self.maturity = maturity
        self.stock_price = stock_price
        self.volatility = volatility
        self.riskfree_rate = riskfree_rate
        self.options = []
    
    def add_new_option(self,
                       option_type:str,
                       strike:float,
                       is_long:bool):
        new_opt = BSPricer(option_type,self.maturity,self.stock_price,strike,self.volatility,self.riskfree_rate,is_long)
        self.options.append(new_opt)
    
    def portfolio_premium(self):
        if not len(self.options):
            raise Exception("Portfolio must contain atleast one option.")
        return sum([option.price_basic_option() for option in self.options])
    
    def portfolio_delta(self):
        if not len(self.options):
            raise Exception("Portfolio must contain atleast one option.")
        return sum([option.get_delta() for option in self.options])
    
    def multi_option_price_run(self):
        if not len(self.options):
            raise Exception("Portfolio must contain atleast one option.")
        option_data = [option.multi_option_price_run() for option in self.options]
        stock_prices = option_data[0]["stock_prices"]
        option_prices = option_data[0]["option_prices"]
        terminal_values = option_data[0]["terminal_values"]
        deltas = option_data[0]["deltas"]

        if len(self.options) == 1:
            return {"stock_prices":stock_prices, 
                    "option_prices":option_prices, 
                    "terminal_values":terminal_values,
                    "deltas":deltas}
        else:
            for idx in range(1,len(self.options)):
                option_prices = [sum(i) for i in zip(option_prices, option_data[idx]["option_prices"])]
                terminal_values = [sum(i) for i in zip(terminal_values, option_data[idx]["terminal_values"])]
                deltas = [sum(i) for i in zip(deltas, option_data[idx]["deltas"])]
            
            return {"stock_prices":stock_prices, 
                    "option_prices":option_prices, 
                    "terminal_values":terminal_values,
                    "deltas":deltas}


        
        
