import os

from dotenv import load_dotenv

from alpha_vantage.timeseries import TimeSeries

from utils5 import StockAnalysis, SMAHandler, SMABackTester

# Load environment variables from .env file
load_dotenv('.env.secret', '.env.shared')

# Access environment variables
API_KEY = os.getenv('ALPHA_API_KEY')
stock = 'NUE'

ts = TimeSeries(key=API_KEY, output_format="pandas")

data, meta_data = ts.get_daily(stock)
print(data.head())

data2 = data["4. close"].to_frame()
close = data2.copy()
close.columns = ['Close']

print(close.head())


analysis = StockAnalysis()
analysis.plot_closes(close)

# Initialize the SMAHandler with the close prices
sma_handler = SMAHandler(close)

# Calculate short-term and long-term SMAs
short_window = 50
long_window = 200
sma_handler.calculate_SMA(short_window, 'SMA_S')
sma_handler.calculate_SMA(long_window, 'SMA_L')

# Generate signals
sma_handler.generate_signals()

# Plot the closing prices along with the SMAs and signals
sma_handler.plot_signals()

# Perform a backtest to evaluate the strategy
start_date=close.index.min()
end_date=close.index.max()
tester=SMABackTester(stock, start_date, end_date, SMA_S=short_window, SMA_L=long_window)

tester.fetch_and_prepare_data()

tester.backtest_strategy()
