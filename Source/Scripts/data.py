import random as rd

import numpy as np
import yfinance as yf
from quandl import ApiConfig, get
from streamlit import cache as stcache, write as stwrite

from Scripts.pages import api_key_string

categories = ['Consumer Staples',
              'Exchange Rates',
              'Energy',
              'Metals',
              'Stocks',
              'Value']

datasets = {
    # The first item in the list, which is the item for each key, symbolises source
    # 'q' : Quandl
    # 'yf' : Yahoo! Finance
    'Cryptocurrencies: Bitcoin GBP': ['BTC-GBP', 'yf'],
    'Cryptocurrencies: Bitcoin USD': ['BTC-USD', 'yf'],
    'Cryptocurrencies: BinanceCoin GBP': ['BNB-GBP', 'yf'],
    'Cryptocurrencies: BinanceCoin USD': ['BNB-USD', 'yf'],
    'Crytpocurrencies: Blockchain': ['BCHAIN/MKPRU', 'q'],
    'Cryptocurrencies: Dogecoin USD' : ['DOGE-USD', 'yf'],
    'Cryptocurrencies: Dogecoin GBP' : ['DOGE-GBP', 'yf'],
    'Cryptocurrencies: Ethereum USD' : ['ETH-USD', 'yf'],
    'Cryptocurrencies: Ethereum GBP' : ['ETH-GBP', 'yf'],
    'Cryptocurrencies: Tether USD' : ['USDT-USD', 'yf'],
    'Cryptocurrencies: Tether GBP' : ['USDT-GBP', 'yf'],
    
    'Exchange Rates: GBP → USD' : ['GBPUSD=X', 'yf'], 
    'Exchange Rates: GBP → EUR' : ['GBPEUR=X', 'yf'],
    
    'Metals: Gold Aug 21' : ['GC=F', 'yf'],
    'Metals: Silver Sep 21' : ['SI=F', 'yf'],
    
    'Indexes: CAC 40' : ['^FCHI', 'yf'],
    'Indexes: CBOE Volatility Index' : ['^VIX', 'yf'],
    'Indexes: CBOE UK 100' : ['^BUK100P', 'yf'],
    'Indexes: Dax Performance' : ['^GDAXI', 'yf'],
    'Indexes: Dow 30' : ['^DJI', 'yf'],
    'Indexes: EURONEXT 100' : ['^N100', 'yf'],
    'Indexes: FTSE 100' : ['^FTSE', 'yf'],
    'Indexes: Jakarta Composite' : ['^JKSE', 'yf'],
    'Indexes: KOSPI Composite' : ['^KS11', 'yf'],
    'Indexes: Nasdaq Composite' : ['^IXIC', 'yf'],
    'Indexes: Nikkei 225' : ['^N225', 'yf'],
    'Indexes: NYSE Composite' : ['^NYA', 'yf'],
    'Indexes: Russel 2000' : ['^RUT', 'yf'],
    'Indexes: S & P 500' : ['^GSPC', 'yf'],
    'Indexes: Treasury Yield 10 Years' : ['^TNX', 'yf'],
    
    'Stocks: Apple Inc.' : ['AAPL', 'yf'],
    'Stocks: Aston Martin Lagonda Global Holdings PLC' : ['AML.L', 'yf'],
    'Stocks: AstraZeneca PLC' : ['AZN', 'yf'],
    'Stocks: AT & T Inc.' : ['T', 'yf'],
    'Stocks: Amazon.com, Inc.' : ['AMZN', 'yf'],
    'Stocks: BMW Group' : ['BMW.DE', 'yf'],
    'Stocks: The Boeing Company' : ['BA', 'yf'],
    'Stocks: The Coca-Cola Company' : ['KO', 'yf'],
    'Stocks: Dell Technologies Inc.' : ['DELL', 'yf'],
    'Stocks: Domino\'s Pizza, Inc.' : ['DPZ', 'yf'],
    'Stocks: Ford Motor Company' : ['F', 'yf'],
    'Stocks: GameStop Corp.' : ['GME', 'yf'],
    'Stocks: Harbour Energy PLC' : ['HBR.L', 'yf'],
    'Stocks: Johnson & Johnson' : ['JNJ', 'yf'],
    'Stocks: Kia Corporation' : ['000270.KS', 'yf'],
    'Stocks: Kellogg Company' : ['K', 'yf'],
    'Stocks: McDonalds Corporation' : ['MDO.HM', 'yf'],
    'Stocks: Microsoft Corporation' : ['MFST', 'yf'],
    'Stocks: Netflix, Inc.' : ['NFLX', 'yf'],
    'Stocks: Nikola' : ['NKLA', 'yf'],
    'Stocks: NIKE, Inc.' : ['NKLA', 'yf'],
    'Stocks: NIO Inc.' : ['NIO', 'yf'],
    'Stocks: Nokia Corporation' : ['NOK', 'yf'],
    'Stocks: Paramount Group, Inc.' : ['PGRE', 'yf'],
    'Stocks: Peleton' : ['PTON', 'yf'],
    'Stocks: Pfizer Inc.' : ['PFE', 'yf'],
    'Stocks: Renewable Energy Group, Inc.' : ['REGI', 'yf'],
    'Stocks: Tesco PLC' : ['TSCDF', 'yf'],
    'Stocks: Tesla, Inc.' : ['TLSA', 'yf'],
    'Stocks: Virgin Galactic Holdings, Inc.' : ['SPCE', 'yf'],
    'Stocks: Volkswagen AG' : ['VWAGY', 'yf'],
    'Stocks: Vodafone Group PLC' : ['VOD', 'yf'],
    'Stocks: Walmart Inc.' : ['WMT', 'yf'],
    'Stocks: The Walt Disney Company' : ['DIS', 'yf'],
    
}

datasets = dict(sorted(datasets.items()))
links = [f'https://finance.yahoo.com/quote/{datasets[key][0]}?p={datasets[key][0]}&.tsrc=fin-srch' for key in datasets]
energy = {}
exchange_rates = {}
metals = {}
stocks = {}
cryptos = {}

for i in datasets:
    if 'Energy:' in i:
        energy = {**energy, i.replace('Energy: ', '') : datasets[i]}
    elif 'Exchange Rates:' in i:
        exchange_rates = {**exchange_rates, i.replace('Exchange Rates: ', '') : datasets[i]}
    elif 'Metals:' in i:
        metals = {**metals, i.replace('Metals: ', '') : datasets[i]}
    elif 'Stocks:' in i:
        stocks = {**stocks, i.replace('Stocks: ', '') : datasets[i]}
    elif 'Cryptocurrencies:' in i:
        cryptos = {**cryptos, i.replace('Cryptocurrencies: ', '') : datasets[i]}

ApiConfig.api_key = 'rkHx96Rssa2DWAeMySeY'

# if api_key_string != '' or api_key_string != ' ':
#     ApiConfig.api_key = api_key_string


def monte_carlo(data_name, column_name, iters=100, reps=100):
    data_data = get_data(data_name)

    column = data_data[column_name]
    curr = column.values[len(column.values)-1]
    all_data = []
    pct_change = column.pct_change()
    incr = 0
    for i in range(len(pct_change)):
        try:
            incr += float((pct_change[i] - pct_change[i+1])/len(pct_change))
        except: break
    stwrite(incr)

    for _ in range(reps):
        out = [curr + curr*rd.normalvariate(incr, 1) for _ in range(iters)]
        all_data.append(out)

    return all_data


@stcache(show_spinner=False)
def get_data(dataset):
    if datasets[dataset][1] == 'q':
        return get(datasets[dataset][0]).replace([0, np.inf,-np.inf], np.nan).interpolate()
    
    elif datasets[dataset][1] == 'yf':
        return yf.download(datasets[dataset][0], period='10y', progress=False).replace([0, np.inf, -np.inf], np.nan).interpolate()