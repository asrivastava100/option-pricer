import numpy as np

class GeometricBrownianMotion:
    def __init__(self, price_start:float, volatility:float, rf_rate:float)->None:
        self.price_start = price_start
        self.volatility = volatility
        self.rf_rate = rf_rate

    def generate_paths(self, time:float, num_paths:int, time_steps:int)->dict:
        normal_sample = np.random.normal(0,1,(num_paths, time_steps))
        dt = time /(time_steps - 1)
        time_axis = np.round(np.linspace(0,time,time_steps),4)
        stock_prices = np.zeros((num_paths,time_steps))
        stock_prices[:,0] = 100

        for idx in range(time_steps-1):
            stock_prices[:,idx+1] = stock_prices[:,idx]*np.exp((self.rf_rate - 0.5 * self.volatility ** 2) * dt + self.volatility * np.sqrt(dt) * normal_sample[:,idx]) 
        return {"stock_prices": stock_prices.tolist(),
                "time_axis": time_axis}


        


    