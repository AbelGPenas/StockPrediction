# get_data_yf.py

# get data directly from Yahoo!Finance using the yfinance module
# data retrieved contains informations about prices of a chosen 'entity' (here S&P500 -> symbol : ^GSPC) :
# Date (timestamp), open, high, low, close, adj close, volume
# data are daily frequency, business days only,  

import pandas as pd
import yfinance as yf

from backtest import Strategy


class Get_data(Strategy):  
    
    def __init__(self, entity, start, end):
        self.start = start
        self.end = end
        self.entity = entity


    def get_raw_prices(self):
        raw = yf.download(self.entity, self.start, self.end)
        return raw


    def raw_to_csv(self):
        raw = yf.download(self.entity, self.start, self.end)
        raw.to_csv("./stocks.csv")
        df = pd.read_csv("stocks.csv", header=[0], index_col=[0], parse_dates=[0]) 
        return df

    
    def get_close_prices(self):
        raw = yf.download(self.entity, self.start, self.end)
 
        # create new DF with dates and Adj Close prices only
        close_series = raw.loc[:, "Adj Close"].copy()    # retrieves only Adj Close prices (but it becomes a pandas Series)
        close_df = pd.DataFrame(close_series)       # converts back the pandas Series into a Dataframe
        return close_df                             # returns a dataframe with Date (as index) and Adj Close prices        
        
