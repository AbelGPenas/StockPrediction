# StockPrediction
This project aims to create an algorithm for investment recommendation based on sentiment analysis of financial news and technical analysis of the indicator of the product targeted.

## NewsScraping
This folder contains the scraping toolkit developed with the scrapy framework. Proxies are imported at teh beggining of each session and only news from the last seven days are scraped. **main.py** can trigger the scrapping action in order to be ready to be implemented into an AWS lambda function.
News are exported as a .json file into an AWS S3 bucket.

## BERT_SentimentAnalysis
A fine-tunned FinBERT model is ussed to assess the polarity of the news headlines and first paragraph.

## Modelling
Some feature engineering work is done with 4 technical variables (moving averages, MACD, RSI and Prophet model). The best performing hyperparameters were selected and the variables used as the input of a deep learning model trained to predict the *next week evolution* of the S&P500. This deep learning model produces as an output a time series with the predicted next-week market movement for each day.

## Backtesting

A toolkit was developed for the backtesting of the strategy advised by the deep learning model. This toolkit produces a log with all the movements and the metrics characterising the finantial performance of the strategy, together with a visualisation of this performance.
