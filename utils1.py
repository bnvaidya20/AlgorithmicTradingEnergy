
import numpy as np 
import yfinance as yf 
import matplotlib.pyplot as plt
import seaborn as sns



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
        self.norm_closes=None
        self.returns=None
        self.summary=None

    def get_closes(self):
        self.closes=self.stocks.loc[:, "Close"].copy()
        return self.closes

    def normalize_closes(self):
        self.norm_closes=self.closes.div(self.closes.iloc[0]).mul(100)

    def calculate_returns(self):
        self.returns = self.closes.pct_change().dropna()
        return self.returns

    def summary_statistics(self):
        self.summary = self.returns.describe().T.loc[:, ["mean", "std"]]
        self.summary["mean"] = self.summary["mean"] * 252  # Annualize mean
        self.summary["std"] = self.summary["std"] * np.sqrt(252)  # Annualize std
        return self.summary

    def plot_normalized_closes(self):
        self.norm_closes.plot(figsize=(15, 8), fontsize=12)
        plt.legend(fontsize=12)
        plt.show()

    def plot_risk_vs_return(self):
        self.summary.plot.scatter(x="std", y="mean", figsize=(12, 8), fontsize=15)
        for i in self.summary.index:
            plt.annotate(i, xy=(self.summary.loc[i, "std"] + 0.002, self.summary.loc[i, "mean"] + 0.002), size=13)
        plt.xlabel("Annual Risk (std)", fontsize=15)
        plt.ylabel("Annual Return", fontsize=15)
        plt.title("Risk vs Return", fontsize=25)
        plt.show()

    def plot_correlation_heatmap(self):
        plt.figure(figsize=(12, 8))
        sns.set_theme(font_scale=1.4)
        sns.heatmap(self.returns.corr(), cmap="Reds", annot=True, annot_kws={"size": 15}, vmax=0.6)
        plt.show()


