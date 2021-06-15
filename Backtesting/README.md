# Backtesting
The backtesting toolkit comprises two classes:
* A BaseBacktesting parent class with all the basic methods.
* A BacktestLogShort class with methods to consider a long-short strategy, simulate it by using a vector of buy/sell (1/-1) signals as argument and return an interactive plot with the backtesting strategy.
## Use example
```python
lsbt = BacktestLongShort(symbol='Close', start='2017-06-15', end='2021-06-14', amount=10000,
datapath='S&P500.csv', verbose=True)
lsbt.run_by_matrix(signals=signals_backtesting, verbose=True, plot_result=True)
```
