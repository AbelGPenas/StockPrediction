# Description
In this initial version the notebook used to develop the features, model and backtesting is openly displayed.
The deep learning model is fed the following technical inputs:
* Moving averages crossing signal.
* MACD signal.
* RSI oversold and overbought signal.
* Prophet model next-week prediction signal.

These variables were optimised by testing the accuracy of the signals emitted.

For the time period with data available, the sentiment data is also available as input.

The deep learning model was trained to predict the next week market evolution with the technical indicators signals as input.

Finally, the strategy was tested with the backtesting toolkit.
