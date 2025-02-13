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
                       is_long:bool) -> None:
        new_opt = BSPricer(option_type,self.maturity,self.stock_price,strike,self.volatility,self.riskfree_rate,is_long)
        self.options.append(new_opt)
    
    def portfolio_premium(self)->float:
        if not len(self.options):
            raise Exception("Portfolio must contain atleast one option.")
        return sum([option.price_basic_option() for option in self.options])
    
    def portfolio_delta(self)->float:
        if not len(self.options):
            raise Exception("Portfolio must contain atleast one option.")
        return sum([option.get_delta() for option in self.options])
    
    def multi_option_price_run(self)->dict:
        if not len(self.options):
            raise Exception("Portfolio must contain atleast one option.")
        option_data = [option.multi_option_price_run() for option in self.options]
        stock_prices = option_data[0]["stock_prices"]
        option_prices = option_data[0]["option_prices"]
        terminal_values = option_data[0]["terminal_values"]
        deltas = option_data[0]["deltas"]
        current_option_price = [option_data[0]["current_option_price"]]
        profit = [i - self.portfolio_premium() for i in terminal_values]

        if len(self.options) == 1:
            return {"stock_prices":stock_prices, 
                    "option_prices":option_prices, 
                    "terminal_values":terminal_values,
                    "deltas":deltas,
                    "current_option_price":current_option_price,
                    "profit":profit}
        else:
            for idx in range(1,len(self.options)):
                option_prices = [sum(i) for i in zip(option_prices, option_data[idx]["option_prices"])]
                terminal_values = [sum(i) for i in zip(terminal_values, option_data[idx]["terminal_values"])]
                deltas = [sum(i) for i in zip(deltas, option_data[idx]["deltas"])]
                current_option_price.append(option_data[idx]["current_option_price"])
            profit = [i - self.portfolio_premium() for i in terminal_values]
            
            return {"stock_prices":stock_prices, 
                    "option_prices":option_prices, 
                    "terminal_values":terminal_values,
                    "deltas":deltas,
                    "current_option_price":current_option_price,
                    "profit":profit}


        
        
