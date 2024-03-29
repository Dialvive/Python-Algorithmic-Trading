# Python Algorithmic Trading

This is a scrap-repository that contains some scripts that follow [@nickmccullum](https://github.com/nickmccullum/)'s [Algorithmic Trading Using Python](https://github.com/nickmccullum/algorithmic-trading-python) course. The purpose of this repository for me has been primarily to learn Python & Algorithmic Trading. I've made this repository public for it to help someone that might be interested in it's contents.

### Dependencies

- pandas
- xlsxwriter
- scipy
- numpy

### Third-party services

- [iexcloud free](https://iexcloud.io): Mock & real data from the stock market.

## Equal Weight S&P500 Trade Recommendations

This script allows the user to get a list of S&P500 stocks, their last prices, and number of shares to acquire given a portfolio size.

### How to run

- Install dependencies,
- `cd eq_weight_S&P_500`,
- create `secrets.py` and add a `IEX_CLOUD_API_TOKEN` variable with a valid iexcloud API key,
- run `python3 equal_weight_S&P_500.py`

## Quantitative Momentum Trade Recommendations

The goal of this script is to delop a investing strategy that recommends an equal weight portfolio of the 50 stocks with the highest price momentum.

### How to run

- Install dependencies,
- `cd quantitative-momentum-strategy`,
- create `secrets.py` and add a `IEX_CLOUD_API_TOKEN` variable with a valid iexcloud API key,
- run `python3 quant_momentum_strategy.py`