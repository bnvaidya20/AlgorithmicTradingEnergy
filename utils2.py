
import pandas as pd 
import yfinance as yf 
import matplotlib.pyplot as plt



class StockDataDownloader:
    def __init__(self, ticker, start_date, end_date):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date

    def fetch_stock_data(self):
        stocks = yf.download(self.ticker, start=self.start_date, end=self.end_date)
        return stocks

class StockAnalysis:
    def __init__(self, stocks):
        self.stocks=stocks
        self.closes=None

    def get_closes(self):
        self.closes=self.stocks.Close.to_frame().copy()
        return self.closes

    def normalize_closes(self):
        return self.closes.div(self.closes.iloc[0]).mul(100)

    def calculate_returns(self):
        return self.closes.pct_change().dropna()
    
    def get_summary(self):
        self.closes=self.closes.copy()
        roll = self.closes.rolling(window=10)
        rollmean = roll.mean()
        rollmed = roll.median()
        rollmax = self.closes.rolling(window=10, min_periods=5).max()
        return rollmean, rollmed, rollmax
    
    def plot_closes(self, stock_name):
        self.closes.plot(figsize=(12, 8), fontsize=15)
        plt.legend(loc="upper left", fontsize=15)
        plt.title(f"Stock {stock_name}")
        plt.show()
    

class SeasonalAnalysis:
        
    def __init__(self, closes):
        self.closes=closes.copy()

    def get_seasonal(self):
        self.closes["Day"] = self.closes.index.day_name()
        self.closes["Quarter"] = self.closes.index.quarter
        return self.closes

    def get_daily_close(self, start_date, end_date, freq="D"):
        # Generate a date range with the correct frequency
        all_days = pd.date_range(start=start_date, end=end_date, freq=freq)
        # Reindex the DataFrame to the new date range and fill missing values by backfilling
        self.closes = self.closes.reindex(all_days).fillna(method="bfill")
        return self.closes
    
    @staticmethod
    def fetch_weekly_stock(stock, interval="1wk"):
        stock = yf.download(stock, interval=interval)
        return stock
    
class RollingStatistics:
    def __init__(self, close_prices):
        self.close_prices = close_prices

    def rolling_means(self, SMA_S, SMA_L):
        if 'Close' in self.close_prices.columns:
            # Ensure the operation is performed on the 'Close' Series
            self.close_prices[f"SMA_{SMA_S}"] = self.close_prices['Close'].rolling(window=SMA_S).mean()
            self.close_prices[f"SMA_{SMA_L}"] = self.close_prices['Close'].rolling(window=SMA_L).mean()
            self.close_prices.dropna(inplace=True)

        else:
            raise KeyError("'Close' column not found in the data")
        return self.close_prices
    
    def plot_closes_sma(self, stock_name, SMA_S, SMA_L):
        sma_s_column = f"SMA_{SMA_S}"
        sma_l_column = f"SMA_{SMA_L}"

        # Plotting the 'Close' prices and SMA
        self.close_prices[['Close', sma_s_column, sma_l_column]].plot(figsize=(12, 8), fontsize=15)
        plt.title(f"For {stock_name}, Close Prices, {sma_s_column} and {sma_l_column}")
        plt.legend(loc="upper left", fontsize=15)
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.show()


    def exponential_moving_average(self, span):
        if 'Close' in self.close_prices.columns:
            # Ensure the operation is performed on the 'Close' Series
            self.close_prices[f"EMA_{span}"] = self.close_prices['Close'].ewm(span=span, min_periods=span).mean()
            self.close_prices=self.close_prices.fillna(method="bfill")
        else:
            raise KeyError("'Close' column not found in the data")
        return self.close_prices

    def plot_closes_ema(self, stock_name, span):
        # Ensure the EMA column name is constructed as a string
        ema_column_name = f"EMA_{span}"

        # Check if the EMA column exists
        if ema_column_name not in self.close_prices.columns:
            raise KeyError(f"{ema_column_name} column not found in the data")

        # Plotting the 'Close' prices and EMA
        self.close_prices[['Close', ema_column_name]].plot(figsize=(12, 8), fontsize=15)
        plt.title(f"For {stock_name}, Close Prices and {ema_column_name}")
        plt.legend(loc="upper left", fontsize=15)
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.show()

