

import config as conf

from utils3 import StockDataHandler, PerformanceMetrics, SMAStrategy

# Cummulative returns , Drawdowns etc

stock="CVX"
handler=StockDataHandler(stock)
cvx_close = handler.fetch_all_stock_data()
print(cvx_close.head())

metrics = PerformanceMetrics(cvx_close, stock)
metrics.calculate_cumulative_returns()
print(cvx_close.head())

cvx_close_sum, cvx_close_exp=metrics.compute_sum_exp()
print(f'Sum: {cvx_close_sum}, EXP: {cvx_close_exp}')

metrics.plot_cumulative_returns()

cvx_close_mean, cvx_close_std=metrics.compute_mean_std()
print(f"Mean: {cvx_close_mean}, STD: {cvx_close_std}")

# Calculate drawdowns

metrics.calculate_drawdowns()
print(cvx_close.head())

metrics.plot_drawdowns()

cvx_close_ddmax, cvx_close_ddmax_day = metrics.get_max_idxmax()
print(f"Max: {cvx_close_ddmax} on day {cvx_close_ddmax_day}")

cvx_close_ddmax_percent, cvx_close_ddmax_percent_day=metrics.get_max_idxmax_percent()
print(f"Max percent: {cvx_close_ddmax_percent} on day {cvx_close_ddmax_percent_day}")



# Simple Moving Average (SMA) strategy

data=cvx_close.loc[(cvx_close.index>="2003-01-01")]
print(data.head())

sma_s=conf.SMA_S
sma_l=conf.SMA_L1

smastrategy=SMAStrategy(data)

smastrategy.apply_sma_strategy(sma_s, sma_l)
print(data.head())

smastrategy.plot_sma_strategy(sma_s, sma_l, stock)
smastrategy.plot_sma_strategy_year(sma_s, sma_l, stock)
smastrategy.plot_sma_with_position(sma_s, sma_l, stock)


results=smastrategy.calculate_performance_metrics()
print(results)


# Strategy adjusted long bias

smastrategy.compute_adjust_long_bias()
print(data.head())

results1=smastrategy.calculate_performance_metrics(column1="ReturnB&H", column2="Strategy2")
print(results1)

results2=smastrategy.calculate_performance_metrics(column1="Strategy", column2="Strategy2")
print(results2)


