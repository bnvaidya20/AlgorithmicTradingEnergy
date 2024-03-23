import numpy as np 
import yfinance as yf 
import matplotlib.pyplot as plt


class StockDataHandler:
    def __init__(self, stock_symbol):
        self.stock_symbol = stock_symbol
        self.data = None

    def fetch_all_stock_data(self):
        self.data = yf.download(self.stock_symbol)
        self.data = self.data.Close.to_frame()
        self.data["D_ret"] = np.log(self.data.div(self.data.shift(1)))
        self.data.dropna(inplace=True)
        return self.data
    
class PerformanceMetrics:
    def __init__(self, data, stock_symbol):
        self.data = data
        self.stock_symbol = stock_symbol  

    def compute_sum_exp(self):
        data_sum =self.data.D_ret.sum()
        data_exp=np.exp(self.data.D_ret.sum())
        return data_sum, data_exp
     
    def compute_mean_std(self):
        data_mean =self.data.D_ret.mean()*252
        data_std=self.data.D_ret.std()*np.sqrt(252)
        return data_mean, data_std
    
    def get_max_idxmax(self):
        data_ddmax=self.data.drawdown.max()
        data_ddmax_day=self.data.drawdown.idxmax()
        return data_ddmax, data_ddmax_day

    def get_max_idxmax_percent(self):
        cvx_close_ddmax_percent=self.data["drawdown%"].max()
        cvx_close_ddmax_percent_day=self.data["drawdown%"].idxmax()
        return cvx_close_ddmax_percent, cvx_close_ddmax_percent_day
    
    def calculate_cumulative_returns(self):
        self.data["cum_ret"] = self.data["D_ret"].cumsum().apply(np.exp)

    def calculate_drawdowns(self):
        self.data["cummax"] = self.data["cum_ret"].cummax()
        self.data["drawdown"] = self.data["cummax"] - self.data["cum_ret"]
        self.data["drawdown%"] = (self.data["drawdown"] / self.data["cummax"]) * 100
    
    def plot_cumulative_returns(self):
        self.data["cum_ret"].plot(figsize=(12, 8), title=f"{self.stock_symbol} Buy & Hold", fontsize=12)
        plt.show()

    def plot_drawdowns(self):
        self.data[["cum_ret", "cummax"]].plot(figsize=(12, 8), title=f"{self.stock_symbol} Cumulative Return & Max", fontsize=12)
        plt.show()

class SMAStrategy:
    def __init__(self, data):
        self.data = data

    def apply_sma_strategy(self, sma_short, sma_long):
        self.data["SMA_S"] = self.data["Close"].rolling(sma_short).mean()
        self.data["SMA_L"] = self.data["Close"].rolling(sma_long).mean()
        self.data.dropna(inplace=True)
        self.data["Position"] = np.where(self.data["SMA_S"] > self.data["SMA_L"], 1, -1)
        self.data["ReturnB&H"]=np.log(self.data.Close.div(self.data.Close.shift(1)))
        self.data["Strategy"] = self.data["ReturnB&H"] * self.data["Position"].shift(1)
        self.data.dropna(inplace=True)

    def calculate_performance_metrics(self, column1="ReturnB&H", column2="Strategy"):
        sma_sum= self.data[[column1, column2]].sum()
        sma_exp= self.data[[column1, column2]].sum().apply(np.exp)
        sma_std= self.data[[column1, column2]].std()*np.sqrt(252)

        results = {
        "sum": sma_sum,
        "exp_sum": sma_exp,
        "annualized_std": sma_std
        }

        return results

    def compute_adjust_long_bias(self):

        self.data["Position2"]=np.where(self.data["SMA_S"]> self.data.SMA_L,1,0)

        self.data["Strategy2"]=self.data["ReturnB&H"]* self.data.Position2.shift(1)

        self.data.dropna(inplace=True)

    def plot_sma_strategy(self, sma_s, sma_l, stock):
        self.data[["Close", "SMA_S", "SMA_L"]].plot(figsize=(12, 8), title="{} - SMA{} | SMA{}".format(stock, sma_s,sma_l), fontsize=12)
        plt.show()
    
    def plot_sma_strategy_year(self, sma_s, sma_l, stock, year="2020"):
        self.data[["Close", "SMA_S", "SMA_L"]].loc[year].plot(figsize=(12, 8), title="{} - SMA{} | SMA{}".format(stock, sma_s,sma_l), fontsize=12)
        plt.show()
    
    def plot_sma_with_position(self, sma_s, sma_l, stock, year="2020"):
        """
        Plots SMA short and SMA long on the primary y-axis and trading positions on the secondary y-axis.

        Parameters:
        - data: DataFrame containing 'SMA_S', 'SMA_L', and 'Position' columns.
        - sma_s: The window size for the short simple moving average.
        - sma_l: The window size for the long simple moving average.
        - stock: stock symbol used.
        - year: The year for which to plot the data. Default is "2020".
        """
        fig, ax1 = plt.subplots(figsize=(12, 8))

        # Plot 'SMA_S' and 'SMA_L' on the primary y-axis
        ax1.plot(self.data.loc["2020", "SMA_S"], color='blue', label=f'SMA_{sma_s}')
        ax1.plot(self.data.loc["2020", "SMA_L"], color='green', label=f'SMA_{sma_l}')
        ax1.set_xlabel('Date', color='g')
        ax1.set_ylabel('SMA_S & SMA_L', color='b')

        # Create a secondary y-axis for 'Position'
        ax2 = ax1.twinx()
        ax2.plot(self.data.loc["2020", "Position"], color='red', label='Position', linestyle='--')
        ax2.set_ylabel('Position', color='r')

        # Title of the plot
        plt.title(f"{stock} - SMA{sma_s} | SMA{sma_l}")

        # Adding legends
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

        # Adjust layout
        plt.tight_layout()

        # Show plot
        plt.show()