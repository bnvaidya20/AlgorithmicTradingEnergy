import numpy as np 
import matplotlib.pyplot as plt
import yfinance as yf 

class SMAHandler:
    def __init__(self, stock):
        self.stock = stock
        self.data = None

    def fetch_stock_data(self, start_date, end_date):
        self.data = yf.download(self.stock, start=start_date, end=end_date)
        return self.data  

    def calculate_SMA(self, SMA_S, SMA_L):
        if self.data is None:
            raise ValueError("Stock data not loaded. Call fetch_stock_data first.")

        data = self.data['Close'].to_frame()
        data['Returns'] = np.log(data['Close'] / data['Close'].shift(1))
        data['SMA_S'] = data['Close'].rolling(SMA_S).mean()
        data['SMA_L'] = data['Close'].rolling(SMA_L).mean()
        data.dropna(inplace=True)
        self.data = data

    def apply_strategy(self):
        if self.data is None or 'SMA_S' not in self.data or 'SMA_L' not in self.data:
            raise ValueError("SMA data not calculated. Call calculate_SMA first.")
        
        # Strategy adjusted long bias
        self.data['Position'] = np.where(self.data['SMA_S'] > self.data['SMA_L'], 1, -1)
        self.data['Strategy'] = self.data['Returns'] * self.data['Position'].shift(1)
        self.data.dropna(inplace=True)

        return self.data
    
    def compute_ret_std(self):

        self.data = self.data.copy()
            
        ret=np.exp(self.data["Strategy"].sum())
        std= self.data["Strategy"].std()*np.sqrt(252)

        return ret, std

class SMABackTester:
    def __init__(self, stock, start_date, end_date, SMA_S, SMA_L):
        self.handler = SMAHandler(stock)
        self.stock=stock
        self.start_date = start_date
        self.end_date = end_date
        self.SMA_S = SMA_S
        self.SMA_L = SMA_L
        self.results = None

    def test_strategy(self):
        self.handler.fetch_stock_data(self.start_date, self.end_date)
        self.handler.calculate_SMA(self.SMA_S, self.SMA_L)
        self.results = self.handler.apply_strategy()

        self.results['ReturnB&H'] = self.results['Returns'].cumsum().apply(np.exp)
        self.results['StrategyResults'] = self.results['Strategy'].cumsum().apply(np.exp)

        perf = self.results['StrategyResults'].iloc[-1]
        outperf = perf - self.results['ReturnB&H'].iloc[-1]

        return round(perf, 6), round(outperf, 6)

    def plot_results(self):
        if self.results is None:
            print("No results to plot. Run the test_strategy method first.")
        else:
            title="{} | SMA_S{} | SMA_L{}".format(self.stock, self.SMA_S, self.SMA_L)
            self.results[["ReturnB&H", "StrategyResults"]].plot(title=title, figsize=(12,8), fontsize=15)
            plt.show()
