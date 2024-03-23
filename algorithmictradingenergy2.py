

import config as conf

from utils2 import StockDataDownloader, StockAnalysis, SeasonalAnalysis, RollingStatistics


"""
Top 3 for Investment

NUE high risk 0.325; high return 0.16
AEP low risk 0.19; better return 0.095
CVX  mid risk 0.28; moderate return 0.085

"""

# Simple Returns and Log Returns

start_date1 = conf.start_date1
end_date1 = conf.end_date1

SMA_S= conf.SMA_S
SMA_L=conf.SMA_L2

span=100

stock1='NUE'

downloader1=StockDataDownloader(stock1, start_date1, end_date1)

stock_nue =downloader1.fetch_stock_data()
print(stock_nue)

analysis1=StockAnalysis(stock_nue)

nue_close=analysis1.get_closes()

returns_nue = analysis1.calculate_returns()
print(returns_nue)

analysis1.plot_closes(stock1)

nue_rollmean, nue_rollmed, nue_rollmax=analysis1.get_summary()
print(nue_rollmean.head(15))
print(nue_rollmed.head(15))
print(nue_rollmax.head(15))

rollstat1=RollingStatistics(nue_close)

nue_close=rollstat1.rolling_means(SMA_S, SMA_L)
print(nue_close.head(10))

# rollstat1.plot_closes_sma(stock1, SMA_S, SMA_L)

span=100
nue_close=rollstat1.exponential_moving_average(span)
print(nue_close.head())

rollstat1.plot_closes_ema(stock1, span)


nue_close1 = stock_nue.Close.to_frame()
print(nue_close1.head())

seasonanalysis=SeasonalAnalysis(nue_close1)

seasonanalysis.get_seasonal()
print(nue_close1.head())

seasonanalysis.get_daily_close(start_date1, end_date1)
print(nue_close1.head())

stock_nue1=seasonanalysis.fetch_weekly_stock(stock1, interval="1wk")
print(stock_nue1)



stock2='AEP'
downloader2=StockDataDownloader(stock2, start_date1, end_date1)
stock_aep =downloader2.fetch_stock_data()
print(stock_aep)

analysis2=StockAnalysis(stock_aep)

aep_close=analysis2.get_closes()

returns_aep = analysis2.calculate_returns()
print(returns_aep)

analysis2.plot_closes(stock2)

aep_rollmean, aep_rollmed, aep_rollmax=analysis1.get_summary()
print(aep_rollmean.head(15))
print(aep_rollmed.head(15))
print(aep_rollmax.head(15))

rollstat2=RollingStatistics(aep_close)

aep_close=rollstat2.rolling_means(SMA_S, SMA_L)
print(aep_close.head(20))

rollstat2.plot_closes_sma(stock2, SMA_S, SMA_L)

aep_close=rollstat2.exponential_moving_average(span)
print(aep_close.head())

rollstat2.plot_closes_ema(stock2, span)


stock3='CVX'
downloader3=StockDataDownloader(stock3, start_date1, end_date1)
stock_cvx =downloader3.fetch_stock_data()
print(stock_cvx)

analysis3=StockAnalysis(stock_cvx)

cvx_close=analysis3.get_closes()

returns_cvx = analysis3.calculate_returns()
print(returns_cvx)

analysis3.plot_closes(stock3)

cvx_rollmean, cvx_rollmed, cvx_rollmax=analysis1.get_summary()
print(cvx_rollmean.head(15))
print(cvx_rollmed.head(15))
print(cvx_rollmax.head(15))

rollstat3=RollingStatistics(cvx_close)

cvx_close=rollstat3.rolling_means(SMA_S, SMA_L)
print(cvx_close.head(20))

rollstat3.plot_closes_sma(stock3, SMA_S, SMA_L)

cvx_close=rollstat3.exponential_moving_average(span)
print(cvx_close.head())

rollstat3.plot_closes_ema(stock3, span)



