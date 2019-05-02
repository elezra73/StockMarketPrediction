#Reference: https://towardsdatascience.com/implementing-moving-averages-in-python-1ad28e636f9d
#Reference: stocks list: https://iextrading.com/apps/stocks/
#Reference: https://github.com/timkpaine/pyEX

import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import pyEX as p
ticker = 'AAPL'
timeframe = '1m'
df = p.chartDF(ticker, timeframe)
df = df[['close']]
df.reset_index(level=0, inplace=True)
df.columns = ['ds','y']
print(df)


print(df)
plt.plot(df.ds, df.y)
plt.show()

rolling_mean = df.y.rolling(window=7).mean()
rolling_mean2 = df.y.rolling(window=14).mean()
plt.plot(df.ds, df.y, label='Apple')
plt.plot(df.ds, rolling_mean, label='Apple 7 Day SMA', color='orange')
plt.plot(df.ds, rolling_mean2, label='Apple 14 Day SMA', color='green')
plt.legend(loc='upper left')
plt.show()