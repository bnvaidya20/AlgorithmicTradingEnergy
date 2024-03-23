
from utils4 import SMAHandler, SMABackTester
import config as conf

StartDate = conf.StartDate 
EndDate = conf.EndDate 
SMA_S= conf.SMA_S
SMA_L1= conf.SMA_L1
SMA_L2=conf.SMA_L2

stock1="XOM"
handler1=SMAHandler(stock1)
data1 = handler1.fetch_stock_data(StartDate, EndDate)
handler1.calculate_SMA(SMA_S, SMA_L2)
data1 = handler1.apply_strategy()
ret1, std1 =handler1.compute_ret_std()
print(f"Return {stock1}: {ret1}, STD {stock1}: {std1} ")

stock2="EOG"
handler2=SMAHandler(stock2)
data2 = handler2.fetch_stock_data(StartDate, EndDate)
handler2.calculate_SMA(SMA_S, SMA_L2)
data2 = handler2.apply_strategy()
ret2, std2 =handler2.compute_ret_std()
print(f"Return {stock2}: {ret2}, STD {stock2}: {std2} ")

stock3="COP"
handler3=SMAHandler(stock3)
data3 = handler3.fetch_stock_data(StartDate, EndDate)
handler3.calculate_SMA(SMA_S, SMA_L2)
data3 = handler3.apply_strategy()
ret3, std3 = handler3.compute_ret_std()
print(f"Return {stock3}: {ret3}, STD {stock3}: {std3} ")

stock4="DUK"
handler4=SMAHandler(stock4)
data4 = handler4.fetch_stock_data(StartDate, EndDate)
handler4.calculate_SMA(SMA_S, SMA_L2)
data4 = handler4.apply_strategy()
ret4, std4 = handler4.compute_ret_std()
print(f"Return {stock4}: {ret4}, STD {stock4}: {std4} ")

stock5="ED"
handler5=SMAHandler(stock5)
data5 = handler5.fetch_stock_data(StartDate, EndDate)
handler5.calculate_SMA(SMA_S, SMA_L2)
data5 = handler5.apply_strategy()
ret5, std5 = handler5.compute_ret_std()
print(f"Return {stock5}: {ret5}, STD {stock5}: {std5} ")

stock6="AEP"
handler6=SMAHandler(stock6)
data6 = handler6.fetch_stock_data(StartDate, EndDate)
handler6.calculate_SMA(SMA_S, SMA_L2)
data6 = handler6.apply_strategy()
ret6, std6 = handler6.compute_ret_std()
print(f"Return {stock6}: {ret6}, STD {stock6}: {std6} ")

stock7="SO"
handler7=SMAHandler(stock7)
data7 = handler7.fetch_stock_data(StartDate, EndDate)
handler7.calculate_SMA(SMA_S, SMA_L2)
data7 = handler7.apply_strategy()
ret7, std7 = handler7.compute_ret_std()
print(f"Return {stock7}: {ret7}, STD {stock7}: {std7} ")




tester=SMABackTester(stock2, StartDate, EndDate, SMA_S, SMA_L1)

perf, outperf=tester.test_strategy()
print(f"Perf: {perf}, Outperf: {outperf} ")

tester.plot_results()


