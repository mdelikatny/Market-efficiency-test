import pandas as pd
import numpy as np
import datetime
import math
from tabulate import tabulate
import matplotlib.pyplot as plt
import seaborn as sns
import pyfolio as pf
import matplotlib
import matplotlib.pyplot as plt
import bs4 as bs
import requests
import yfinance as yf
from scipy import stats
from statsmodels.tsa.stattools import adfuller

# Define a function to calculate market efficiency for a given stock ticker
def marketEfficency_df(tick, data1):
    # Create a DataFrame with OHLC data
    df = pd.DataFrame()
    df['Open ' + tick] = data1['Open'][tick]
    df['High' + tick] = data1['High'][tick]
    df['Low ' + tick] = data1['Low'][tick]
    df['Close' + tick] = data1['Close'][tick]
    df['Adj Close' + tick] = data1['Adj Close'][tick]
    df['Volume' + tick] = data1['Volume'][tick]
    df.columns = ['Open', 'High','Low', 'Close','Adj Close','Volume']
    
    # Calculate the daily percentage change, mean, and sigma
    df['daily_pct_change'] = df['Adj Close'].pct_change()
    mu = df['daily_pct_change'].iloc[:-252].mean()
    sigma = df['daily_pct_change'].iloc[:-252].std()
    
    # Generate a simulation of the probable price path using a random walk simulation
    simulation = {}
    simulation['Actual'] = list(df['Adj Close'].iloc[-252:].values)
    for sim in range(1, 5): # Taking 5 paths
        simulation["Simulation_"+str(sim)] = [df['Adj Close'].iloc[-252]]
        for days in range(251):
            next_day = simulation["Simulation_"+str(sim)][-1] * np.exp((mu - (sigma**2/2)) + sigma * np.random.normal())
            simulation["Simulation_"+str(sim)].append(next_day)
        
    # Compute the F-value and p-value of the ANOVA test on the simulation data to determine market efficiency
    simulation = pd.DataFrame(simulation)
    F, p = stats.f_oneway(simulation['Actual'], simulation['Simulation_1'], simulation['Simulation_2'], simulation['Simulation_3'], simulation['Simulation_4'])
    msg = "%s: %f: %.2E: " % (tick, F, p)
    print(msg)

    return p

# Read a CSV file that contains a list of stock tickers
newtickers = pd.read_csv('highmidlow90tickers.csv')
newtickers = newtickers.values.tolist()

# Loop over each ticker and calculate its market efficiency
for i in range(0, len(newtickers)):
    tick = newtickers[i]
    df = marketEfficency_df(tick, data1)

# Define a function to test for stationarity using the Augmented Dickey-Fuller (ADF) test
def dickyfullermethod(tick, data1):
    # Create a DataFrame with the Adj Close column
    df = pd.DataFrame()
    df['Adj Close' + tick] = data1['Adj Close'][tick]
    
    # Replace infinity and NaN values with 0
    adj = df.replace([np.inf, -np.inf], np.nan).fillna(0)
    
    # Compute the log of the Adj Close column
       X = log(adj).replace([np.inf, -np.inf], np.nan).fillna(0)
    
    # Run the Augmented Dickey-Fuller (ADF) test to check for stationarity of the stock
    result = adfuller(X, autolag='AIC')
    print('ticker: %s' % tick)
    print('ADF Statistic: %f' % result[0])
    print('p-value: %f' % result[1])
    print('Critical Values:')
    for key, value in result[4].items():
        print('\t%s: %.3f' % (key, value))
        
    return result[0]

# Loop over each ticker and test for stationarity using the ADF test
Dickyfullerresults = pd.DataFrame()
for i in range(0, len(newtickers)):
    tick = newtickers[i]
    df = dickyfullermethod(tick, data1)
    # Dickyfullerresults.insert(i, "stock", result[0], True)
    
# Dickyfullerresults.newcolumns = newtickers

