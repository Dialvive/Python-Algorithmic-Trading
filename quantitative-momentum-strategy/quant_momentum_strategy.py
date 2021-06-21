# *************************************************************************************************
# quant_momentum_strategy
#
# The goal of this script is to delop a investing strategy that recommends an equal weight
# portfolio of the 50 stocks with the highest price momentum.
# 
# Following @nickmccullum Algorithmic Trading in Python course. Available at:
# https://github.com/nickmccullum/algorithmic-trading-python
# 
# API documentation: https://iexcloud.io/docs/api/

import numpy
import pandas
import requests
import math
from scipy import stats
import xlsxwriter

stocks = pandas.read_csv('sp_500_stocks.csv')

from secrets import IEX_CLOUD_API_TOKEN # variable in secret file

symbol = 'AAPL'
api_url = f'https://sandbox.iexapis.com/stable/stock/{symbol}/stats/?token={IEX_CLOUD_API_TOKEN}'
data = requests.get(api_url).json()

# GET stock data from IEX API in batches ######################################
def chunks(lst, n):
    '''Yield succesive n-sized chinks from lst.'''
    for i in range(0, len(lst), n):
        yield lst[i:i+n]

stock_chunks = list(chunks(stocks['Ticker'], 100)) #Chunkify stocks for batch api calls
stock_strings = []
for i in range(0, len(stock_chunks)):
    stock_strings.append(','.join(stock_chunks[i]))

# Create DataFrame
dataframe_columns = ['Ticker', 'Stock Price', 'One-Year Price Return', 'Shares to Buy']
dataframe = pandas.DataFrame(columns = dataframe_columns)

for stock_string in stock_strings: # GET all stock stats
    batch_api_call_url = f'https://sandbox.iexapis.com/stable/stock/market/batch/?symbols={stock_string}&types=price,stats&token={IEX_CLOUD_API_TOKEN}'
    data = requests.get(batch_api_call_url).json()
    for stock in stock_string.split(','): #Fill each stock row in the dataframe
        dataframe = dataframe.append( 
            pandas.Series(
                [
                    stock,                                       #Ticker
                    data[stock]['price'],                        #Stock price
                    data[stock]['stats']['year1ChangePercent'],  #One-Year Price Return
                    'N/A'                                        #Shares to Buy
                ], 
                index = dataframe_columns
            ),
            ignore_index = True
        )

# Removing low momentum stocks ################################################

dataframe.sort_values('One-Year Price Return', ascending = False, inplace = True)
dataframe = dataframe[:50]
dataframe.reset_index(inplace = True)

# Calculate the number of shares to buy #######################################
def get_portfolio_size():
    portfolio_incorrect = True
    while portfolio_incorrect:
        portfolio_size = input('Enter value of portfolio: ') #Calculate number of shares to buy
        try:
            portfolio_size = float(portfolio_size)
            portfolio_incorrect = False
        except ValueError:
            print('Error: Enter a number! \n')
    return portfolio_size

position_size = get_portfolio_size() / len(dataframe.index)
for i in range(0, len(dataframe)):
    dataframe.loc[i, 'Shares to Buy'] = math.floor(position_size / dataframe.loc[i, 'Stock Price'])
print(dataframe)