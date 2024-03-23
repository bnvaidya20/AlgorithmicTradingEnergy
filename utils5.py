import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt

import os
from dotenv import load_dotenv
from alpha_vantage.timeseries import TimeSeries


# Load environment variables from .env file
load_dotenv()

# Access environment variables
API_KEY = os.getenv('ALPHA_API_KEY')

class StockAnalysis:

    @staticmethod
    def summary_statistics(returns):
        summary = returns.describe().T.loc[:, ["mean", "std"]]
        summary["mean"] = summary["mean"] * 252  # Annualize mean
        summary["std"] = summary["std"] * np.sqrt(252)  # Annualize std
        return summary

    @staticmethod
    def plot_closes(closes):
        closes.plot(figsize=(15, 8), fontsize=12)
        plt.legend(fontsize=12)
        plt.show()


class SMAHandler:
    def __init__(self, data):
        if isinstance(data, pd.DataFrame):
            self.data = data
        else:
            raise TypeError("Data must be a pandas DataFrame")

    def calculate_SMA(self, window, column_name):
        if 'Close' in self.data.columns:
            self.data[column_name] = self.data['Close'].rolling(window=window).mean()
        else:
            raise KeyError("'Close' column not found in the data")


    def generate_signals(self):
        # Generate buy/sell signals
        self.data['Signal'] = 0  # Default to no position
        self.data.loc[self.data['SMA_S'] > self.data['SMA_L'], 'Signal'] = 1  # Go long
        self.data.loc[self.data['SMA_S'] < self.data['SMA_L'], 'Signal'] = -1  # Go short

        self.data['Position'] = self.data['Signal'].diff()  # Change in position


    def plot_signals(self):
        # Plot the closing prices, SMAs, and buy/sell signals
        plt.figure(figsize=(14, 7))

        # Plot closing prices
        plt.plot(self.data.index, self.data['Close'], label='Close Prices', alpha=0.5)

        # Plot short-term and long-term SMAs
        plt.plot(self.data.index, self.data['SMA_S'], label=f'Short-term SMA', alpha=0.75)
        plt.plot(self.data.index, self.data['SMA_L'], label=f'Long-term SMA', alpha=0.75)

        # Plot buy signals
        plt.plot(self.data[self.data['Position'] == 1].index, 
                self.data['SMA_S'][self.data['Position'] == 1], 
                '^', markersize=10, color='g', lw=0, label='Buy Signal')

        # Plot sell signals
        plt.plot(self.data[self.data['Position'] == -1].index, 
                self.data['SMA_S'][self.data['Position'] == -1], 
                'v', markersize=10, color='r', lw=0, label='Sell Signal')

        plt.title('Stock Price and SMA Crossovers')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend(loc='best')
        plt.show()




class SMABackTester:
    def __init__(self, stock_symbol, start_date, end_date, SMA_S, SMA_L):
        self.stock_symbol = stock_symbol
        self.start_date = start_date
        self.end_date = end_date
        self.SMA_S = SMA_S
        self.SMA_L = SMA_L
        self.results = None
        self.data = None  # Initialize an attribute to hold the stock data

        self.fetch_and_prepare_data()  # Fetch and prepare the data
        self.handler = SMAHandler(self.data)  # Initialize the handler with the data

    def fetch_and_prepare_data(self):
        # Assuming TimeSeries is already set up with an API key
        ts = TimeSeries(key=API_KEY, output_format="pandas")
        data, meta_data = ts.get_daily(self.stock_symbol, outputsize='full')
        self.data = data["4. close"].to_frame()
        self.data.columns = ['Close']  # Rename the column to 'Close'
        self.data.dropna(inplace=True)  # Ensure there are no NaN values

    def backtest_strategy(self):
        # Ensure that SMAs are calculated and signals are generated
        self.handler.calculate_SMA(self.SMA_S, 'SMA_S')
        self.handler.calculate_SMA(self.SMA_L, 'SMA_L')
        self.handler.generate_signals()

        # Update self.data with the processed data from the handler
        self.data = self.handler.data

        # Check if 'Signal' column exists
        if 'Signal' not in self.data.columns:
            raise KeyError("'Signal' column not found. Ensure that generate_signals method has been called.")

        # Calculate strategy returns
        self.data['Strategy_Return'] = self.data['Signal'].shift(1) * self.data['Close'].pct_change()
        self.data['Cumulative_Strategy_Return'] = (1 + self.data['Strategy_Return']).cumprod()

        # Calculate buy and hold returns
        self.data['Buy_Hold_Return'] = self.data['Close'].pct_change()
        self.data['Cumulative_Buy_Hold_Return'] = (1 + self.data['Buy_Hold_Return']).cumprod()

        # Now that 'Cumulative_Buy_Hold_Return' is calculated, it's safe to call plot_results
        self.plot_results()

    def plot_results(self):
        if 'Cumulative_Buy_Hold_Return' not in self.data.columns:
            raise KeyError("'Cumulative_Buy_Hold_Return' column not found. Ensure it is calculated before plotting.")

        plt.figure(figsize=(12, 8))
        plt.plot(self.data['Cumulative_Strategy_Return'], label='Strategy Returns')
        plt.plot(self.data['Cumulative_Buy_Hold_Return'], label='Buy & Hold Returns')
        plt.title('Backtest Results')
        plt.xlabel('Date')
        plt.ylabel('Cumulative Returns')
        plt.legend()
        plt.show()


