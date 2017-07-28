#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  8 21:38:33 2017

@author: yanghehuo
"""

import quandl
import numpy as np
import pandas as pd

#Ticket = 'WIKI/AAPL'
#steps = 5
#paths = 1000

def GetQuotes(ticket):
    aapl = quandl.get(ticket, start_date='2010-01-01', end_date='2012-01-01')
    quotes = aapl
    return quotes

def AddReturns(quotes):
    quotes['Returns'] = np.log(quotes['Adj. Close']/quotes['Adj. Close'].shift(1))
    return quotes

def MonteCarlo(quotes, paths, steps):

    # Historical volatility
    vol = np.std(quotes['Returns'])
    dailyReturn = quotes['Returns'].mean()

    SimulationStartDate = quotes.index[-1]

    daterng = pd.bdate_range(SimulationStartDate, periods=steps + 1)

    # create an empty DataFrame to store the paths: P paths and N steps
    SimulationPaths = pd.DataFrame(index = daterng, columns = range(paths))

    # Set initial value in the simulation equal to the last available closing quote
    SimulationPaths.loc[SimulationStartDate] = np.full(paths, quotes.iloc[-1][10])

    for j in range(paths):
        for i in range(1,steps+1):
            SimulationPaths.iloc[i,j] = SimulationPaths.iloc[i-1,j] * \
            GBM_path(dailyReturn, vol, 1)

    return SimulationPaths

def GBM_path(u,v,t):
    # Brownean Motion with drift rate expressed as: Drift mean = Drift daily - 0.5*daily vol ^2
    rand = np.random.randn()
    price_increment = np.exp((u - 0.5 * v ** 2)*t + v * np.sqrt(t) * rand)
    
    return price_increment

# order results and get the VAR value at the confidence interval

def VAR(SimulationPaths,confidence,stock,day):
    resulting_value = SimulationPaths.iloc[-1:]
    p = confidence * 100
    VAR = np.percentile(resulting_value,q=p,interpolation='lower')
    output = stock+' '+str(day)+' day VAR at confidence level of '+ \
    str(confidence) + ' is ' + str(round(VAR,2))
    
    return output

Quotes = GetQuotes(ticket = 'WIKI/AAPL')
CleanQuotes = AddReturns(Quotes)
montecarloSimulation = MonteCarlo(quotes = CleanQuotes, paths =1000, steps=5)
Var = VAR(SimulationPaths = montecarloSimulation,confidence = 0.05, stock = 'AAPL', day = 5)

print (Var)

print (montecarloSimulation.plot(legend=False))










