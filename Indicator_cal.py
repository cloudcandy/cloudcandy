#Import the libraries
import pyupbit
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

def SMA(data, period=30, column='close'):
  return data[column].rolling(window=period).mean()

#Create the Exponential Moving Average Indicator
def EMA(data, period=20, column='close'):
  return data[column].ewm(span=period, adjust=False).mean()

def MACD(data, period_long=26, period_short=12, period_signal=9, column='close'):
    #Calculate the Short Term Exponential Moving Average
    ShortEMA = EMA(data, period_short, column=column) #AKA Fast moving average
    #Calculate the Long Term Exponential Moving Average
    LongEMA = EMA(data, period_long, column=column) #AKA Slow moving average
    #Calculate the Moving Average Convergence/Divergence (MACD)
    data['MACD'] = ShortEMA - LongEMA
    #Calcualte the signal line
    data['Signal_Line'] = EMA(data, period_signal, column='MACD')#data['MACD'].ewm(span=period_signal, adjust=False).mean()
        
    return data

#Create RSI function
def RSI(data, period = 14, column = 'close'):
  delta = data[column].diff(1) #Use diff() function to find the discrete difference over the column axis with period value equal to 1
  delta = delta.dropna() # or delta[1:]
  up =  delta.copy() #Make a copy of this object’s indices and data
  down = delta.copy() #Make a copy of this object’s indices and data
  up[up < 0] = 0 
  down[down > 0] = 0 
  data['up'] = up
  data['down'] = down
  AVG_Gain = SMA(data, period, column='up')#up.rolling(window=period).mean()
  AVG_Loss = abs(SMA(data, period, column='down'))#abs(down.rolling(window=period).mean())
  RS = AVG_Gain / AVG_Loss
  RSI = 100.0 - (100.0/ (1.0 + RS))
  
  data['RSI'] = RSI
  return data

df = pyupbit.get_ohlcv(ticker="KRW-ETC",interval="minute5",count=100)

MACD(df)
RSI(df)
df['SMA'] = SMA(df)
df['EMA'] = EMA(df)
#Show the data
df

#Plot the chart
#Create a list of columns to keep
column_list = ['MACD','Signal_Line']
df[column_list].plot(figsize=(12.2,6.4)) #Plot the data
plt.title('MACD for TSLA')
plt.show()

#Plot the chart
#Create a list of columns to keep
column_list = ['SMA','close']
df[column_list].plot(figsize=(12.2,6.4)) #Plot the data
plt.title('SMA for TSLA')
plt.ylabel('USD Price ($)')
plt.show()

#Plot the chart
#Create a list of columns to keep
column_list = ['EMA','close']
df[column_list].plot(figsize=(12.2,6.4)) #Plot the data
plt.title('EMA for TSLA')
plt.ylabel('USD Price ($)')
plt.show()

#Plot the chart
#Create a list of columns to keep
#Sell: RSI = 70 or greater
#Buy: RSI = 30 or lower
column_list = ['RSI']
df[column_list].plot(figsize=(12.2,6.4)) #Plot the data
plt.title('RSI for TSLA')
plt.show()