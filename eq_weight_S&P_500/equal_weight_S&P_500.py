# *************************************************************************************************
# equal_weight_S&P_500
#
# The goal of this script is to tell how many shares of each S&P 500 constituent you should 
# purchase to get an equal weight version of the S&P 500.
# 
# Following @nickmccullum Algorithmic Trading in Python course. Available at:
# https://github.com/nickmccullum/algorithmic-trading-python


import numpy
import pandas
import requests
import xlsxwriter
import math

stocks = pandas.read_csv('sp_500_stocks.csv')

from secrets import IEX_CLOUD_API_TOKEN # variable in secret file

dataframe_columns = ['Ticker', 'Stock Price', 'Shares to buy']

# Get portfolio size ##########################################################
portfolio_incorrect = True
while portfolio_incorrect:
    portfolio_size = input('Enter value of portfolio:') #Calculate number of shares to buy
    try:
        portfolio_size = float(portfolio_size)
        portfolio_incorrect = False
    except ValueError:
        print('Error: Enter an integer! \n')

# GET single stock data from IEX API ##########################################
#symbol = 'AAPL'
#api_url = f'https://sandbox.iexapis.com/stable/stock/{symbol}/quote/?token={IEX_CLOUD_API_TOKEN}'
#data = requests.get(api_url).json()
#price = data['latestPrice']
#dataframe = pandas.DataFrame(columns = dataframe_columns)
#dataframe = dataframe.append(
#    pandas.Series(
#        [symbol, price, 'N/A'],
#        index = dataframe_columns
#    ),
#    ignore_index=True
#)
#print(dataframe)

# GET multiple stock data from IEX API ########################################
#dataframe = pandas.DataFrame(columns = dataframe_columns)
#for stock in stocks['Ticker']:
#    api_url = f'https://sandbox.iexapis.com/stable/stock/{stock}/quote/?token={IEX_CLOUD_API_TOKEN}'
#    data = requests.get(api_url).json()
#    dataframe = dataframe.append(
#    pandas.Series(
#        [stock, data['latestPrice'], 'N/A'],
#        index = dataframe_columns
#    ),
#    ignore_index=True
#)
#print(dataframe)

# GET stock data from IEX API in batches ######################################

def chunks(lst, n):
    '''Yield succesive n-sized chinks from lst.'''
    for i in range(0, len(lst), n):
        yield lst[i:i+n]

stock_chunks = list(chunks(stocks['Ticker'], 100)) #Chunkify stocks for batch api calls
stock_strings = []
for i in range(0, len(stock_chunks)):
    stock_strings.append(','.join(stock_chunks[i]))

dataframe = pandas.DataFrame(columns = dataframe_columns)
for stock_string in stock_strings: #Request to API per chunk
    batch_api_call_url = f'https://sandbox.iexapis.com/stable/stock/market/batch?symbols={stock_string}&types=quote&token={IEX_CLOUD_API_TOKEN}'
    data = requests.get(batch_api_call_url).json()
    for stock in stock_string.split(','): #De-chunkify api response
        dataframe = dataframe.append(
        pandas.Series(
            [stock, data[stock]['quote']['latestPrice'], 'N/A'],
            index = dataframe_columns
        ),
        ignore_index=True
    )

position_size = portfolio_size / len(dataframe.index) #Money to invest per stock
for i in range(0, len(dataframe.index)):
    dataframe.loc[i, 'Shares to buy'] = math.floor(position_size / dataframe.loc[i, 'Stock Price'])

# Format data as Excel file ###################################################
writer = pandas.ExcelWriter('recommended_trades.xlsx', engine="xlsxwriter")
dataframe.to_excel(writer, 'Recommended Trades', index=False)

background_color = '#0a0a23'
font_color = '#ffffff'

# Cell formats
string_format = writer.book.add_format(
    {
        'font_color':font_color, 
        'bg_color':background_color, 
        'border':1
    }
)

dollar_format = writer.book.add_format(
    {
        'num_format': '$0.00',
        'font_color':font_color, 
        'bg_color':background_color, 
        'border':1
    })

integer_format = writer.book.add_format(
    {
        'num_format': '0',
        'font_color':font_color, 
        'bg_color':background_color, 
        'border':1
    })

column_formats = {
    'A':['Ticker', string_format],
    'B':['Stock Price', dollar_format],
    'C':['Shares to buy', integer_format]
}

for column in column_formats.keys():
    writer.sheets['Recommended Trades'].set_column(f'{column}:{column}', 18, column_formats[column][1])
    writer.sheets['Recommended Trades'].write(f'{column}1', column_formats[column][0], column_formats[column][1])
writer.save()
