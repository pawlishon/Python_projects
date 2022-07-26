import pandas as pd
import json
import numpy as np

# Testing whether Capital Asset Pricing Model works. If there are linear dependency between beta and yearly return. Data downloaded through yfapi.py which uses yahoo finance api.
sp500 = pd.read_excel('sp500.xlsx')

# Connecting data from jsons
file_data = {}
for ticker in sp500.symbol.to_list():
    file = open(f'QuoteSummaries/{ticker}.json')
    data = json.load(file)
    try:
        beta = data['defaultKeyStatistics']['beta']['raw']
    except:
        beta = np.NaN
    try:
        year_profit = data['defaultKeyStatistics']['52WeekChange']['raw']
    except:
        year_profit = np.NaN
    file_data[ticker] = {'beta': beta, 'year profit': year_profit}

sp500['beta'] = sp500['symbol'].apply(lambda x: file_data[x]['beta'])
sp500['52WeekChange'] = sp500['symbol'].apply(lambda x: file_data[x]['year profit'])

import matplotlib.pyplot as plt

plt.scatter(sp500['beta'], sp500['52WeekChange'] )
plt.show()

# Removing outliers
chart_table = sp500.loc[(sp500['beta'] < 4) & (sp500['trailingPE'] < 350), ['beta', 'trailingPE', '52WeekChange']]


plt.scatter(chart_table['beta'], chart_table['52WeekChange'] )
plt.show()

# Grouping data to decils
chart_table = chart_table.sort_values(by='beta')
chart_table = chart_table.reset_index()
chart_table['index'] = chart_table.index / 50
import math
chart_table['index'] = chart_table['index'].apply(lambda x: math.modf(x)[1])
avgs = chart_table.groupby(['index']).mean()
plt.scatter(avgs['beta'], avgs['52WeekChange'] )
plt.show() # No linear dependency between year profit and beta. Safer stock are doing better

chart_table['52WeekChange'].mean() # On average stocks lost 6% in last year as of July 2022