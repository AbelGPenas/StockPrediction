# movingaverage_cross.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
from datetime import date
from dateutil.relativedelta import relativedelta

from backtest import Strategy
from get_data_yf import Get_data


# how to generate the signs {1, 0, -1} when the moving averages (short and long) of "entity" cross over each other.
# from these signs we can add indicators on the trend graph to better visualize the uptrends/downtrends.


class MovingAverageStrategy(Strategy):

# Note:
# sma_short = short term SMA
# sma_long = long term SMA
# The idea is to construct and plot them both on the same graph. 
# It helps taking trading decisions, by giving, graphically, an idea of an eventual trend.
# If the long-term average is above the shorter-term average then a downtrend might be expected,
# and vice-versa
    
    def __init__(self, entity, candles, sma_short=50, sma_long=200):
        self.entity = entity
        self.candles = candles
        self.sma_short = sma_short
        self.sma_long = sma_long
        
    def generate_signs(self):
        # return dataframe of signs {1, 0, -1}
        
        signs = pd.DataFrame(index=self.candles.index)
        
        # create new column "sign" with values initially set to 0.0        
        signs['sign'] = 0.0
        
        signs['short_sma'] = candles.Close.rolling(window=self.sma_short, min_periods=30).mean()
        
        signs['long_sma'] = candles.Close.rolling(window=self.sma_long, min_periods=30).mean()
        
        signs.dropna(inplace=True)
        
        # new column "sign" : value is set to 1.0 when short MA > long MA, and kept 0.0 otherwise
        signs['sign'][self.sma_short:] = np.where(signs['short_sma'][self.sma_short:] 
            > signs['long_sma'][self.sma_short:], 1.0, 0.0)
        
        # take difference of the signs to get actual trading orders
        signs['position'] = signs['sign'].diff()   

        #signs.position.to_csv("./SignS.csv")   #check
        
        return signs
    

  
    
if __name__ == "__main__":

    # data setup
   
    entity = '^GSPC'    # S&P500's symbol
    t1 = 5              # FROM t1 years ago (start date)
    #t2 = 1             # TO t2 years ago (end date)
    start = (date.today()+relativedelta(years=-t1)).strftime("%Y-%m-%d")    # 'yyyy-mm-dd' format
    end = time.strftime("%Y-%m-%d")     # today
    #end = (date.today()+relativedelta(years=-t2)).strftime("%Y-%m-%d")

    get_it = Get_data(entity, start, end)
    candles = get_it.get_raw_prices()


    # call the strategy

    mavg_strategy = MovingAverageStrategy(entity, candles, sma_short=50, sma_long=200)
    signs = mavg_strategy.generate_signs()


    # Long SMA / Short SMA Crossing strategy GRAPH
    
    # Plot two charts to assess trades and equity curve
    fig = plt.figure()
    plt.rcParams['figure.figsize']=(25, 10)
    fig.patch.set_facecolor('white')
    ax = fig.add_subplot(211,  ylabel='Adj Close Prices in $')
    
    
    # Plot the GSPC adj closing price overlaid with the moving averages
    candles['Adj Close'].plot(ax=ax, color='k', lw=1.)
    signs[['short_sma', 'long_sma']].plot(ax=ax, lw=1.)


    # Plot the "buy" trades
    ax.plot(signs.loc[signs.position == 1.0].index, 
             signs.short_sma[signs.position == 1.0],
             '^', markersize=9, color='g')

    # Plot the "sell" trades
    ax.plot(signs.loc[signs.position == -1.0].index, 
             signs.short_sma[signs.position == -1.0],
             'v', markersize=9, color='r')
    plt.title('S&P500 adj close prices')

    # Plot the figure
    fig.show()
