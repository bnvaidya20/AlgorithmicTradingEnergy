

import config as conf

from utils1 import StockDataDownloader, StockAnalysis


# Energy Trading


"""
Energy companies by stock price

Nucor Corporation                   - NUE       174.22
Chevron                             - CVX       149.68
EOG Resources Inc                   - EOG       121.62
ConocoPhillips                      - COP       114.90
Exxon Mobil                         - XOM       101.65
Duke Energy Corp                    - DUK       97.17 
Consolidated Edison, Inc.           - ED        90.00
American Electric Power Company Inc - AEP       81.73
Southern Co                         - SO        71.42
TotalEnergies                       - TTE       67.73
Shell                               - SHEL      64.71
TC Energy Corp                      - TRP       38.99
Enbridge Inc                        - ENB       35.51
BP                                  - BP        35.12

"""

# Access environment variables
start_date = conf.start_date
end_date = conf.end_date

ticker_et = ["XOM", "CVX", "COP", "SHEL", "TTE", "BP", "ENB", "EOG", "TRP", "AEP", "SO", "ED", "DUK", "NUE"]

downloader=StockDataDownloader(ticker_et, start_date, end_date)

stocks_et =downloader.fetch_stock_data()
print(stocks_et.head())
print(stocks_et.info())
print(stocks_et.describe())

stockanalysis=StockAnalysis(stocks_et)

closes_et=stockanalysis.get_closes()
print(closes_et.head())

stockanalysis.normalize_closes()

stockanalysis.plot_normalized_closes()

ret_et=stockanalysis.calculate_returns()
print(ret_et)

summary_et=stockanalysis.summary_statistics()
print(summary_et)

stockanalysis.plot_risk_vs_return()

# Correlation and covariance

print(ret_et.cov())

print(ret_et.corr())

stockanalysis.plot_correlation_heatmap()