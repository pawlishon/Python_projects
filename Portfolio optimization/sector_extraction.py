import pandas as pd
import yfinance as yf

prices = pd.read_excel('ETF_data_revolut.xlsx')
prices.set_index('Date', inplace=True)

tickers = list(prices.columns)[-15:]

sectors = []
for tick in tickers:
    ticker = yf.Ticker(tick)
    info = ticker.get_info()
    try:
        sectors.append([tick, info['longName']])
    except KeyError:
        sectors.append([tick, 'N/A'])

sectors_1 = pd.DataFrame(sectors, columns = ['Ticker', 'Long name'])
sectors_2 = pd.DataFrame(sectors, columns = ['Ticker', 'Long name'])
sectors_3 = pd.DataFrame(sectors, columns = ['Ticker', 'Long name'])

sectors_df = pd.concat([sectors_1, sectors_2, sectors_3]).drop_duplicates()
sectors_df.to_csv('long_names.csv')
sectors_df = pd.read_csv('long_names.csv')
sectors_df.drop(sectors_df.columns[0], axis=1, inplace=True)

sectors_df['Long name'] = sectors_df['Long name'].str.upper()

import numpy as np

sectors_df['Sector'] = 'Other'
sectors_df['Country'] = 'Other'
sectors_df['Sector'] = np.where(sectors_df['Long name'].str.contains('BOND'), 'BOND', sectors_df['Sector'])
sectors_df['Sector'] = np.where(sectors_df['Long name'].str.contains('YIELD'), 'BOND', sectors_df['Sector'])
sectors_df['Sector'] = np.where(sectors_df['Long name'].str.contains('HEALTHCARE'), 'HEALTHCARE', sectors_df['Sector'])
sectors_df['Country'] = np.where(sectors_df['Long name'].str.contains('FTSE'), 'GB', sectors_df['Country'])
sectors_df['Country'] = np.where(sectors_df['Long name'].str.contains(' USA '), 'US', sectors_df['Country'])
sectors_df['Country'] = np.where(sectors_df['Long name'].str.contains(' US '), 'US', sectors_df['Country'])
sectors_df['Country'] = np.where(sectors_df['Long name'].str.contains('WORLD'), 'WORLD', sectors_df['Country'])
sectors_df['Country'] = np.where(sectors_df['Long name'].str.contains('EUROPE'), 'EUROPE', sectors_df['Country'])
sectors_df['Country'] = np.where(sectors_df['Long name'].str.contains('S&P 500'), 'US', sectors_df['Country'])
sectors_df['Country'] = np.where(sectors_df['Long name'].str.contains('JAPAN'), 'JAPAN', sectors_df['Country'])
sectors_df['Country'] = np.where(sectors_df['Long name'].str.contains('CHINA'), 'CHINA', sectors_df['Country'])
sectors_df['Sector'] = np.where(sectors_df['Long name'].str.contains('MORTGAGE'), 'MORTGAGE', sectors_df['Sector'])
sectors_df['Country'] = np.where(sectors_df['Long name'].str.contains('GERMANY'), 'GERMANY', sectors_df['Country'])
sectors_df['Sector'] = np.where(sectors_df['Long name'].str.contains('COPPER'), 'COMMODITIES', sectors_df['Sector'])
sectors_df['Sector'] = np.where(sectors_df['Long name'].str.contains('METALS'), 'COMMODITIES', sectors_df['Sector'])
sectors_df['Sector'] = np.where(sectors_df['Long name'].str.contains('TECH'), 'TECHNOLOGY', sectors_df['Sector'])
sectors_df['Sector'] = np.where(sectors_df['Long name'].str.contains('FINANCIAL'), 'FINANCIAL', sectors_df['Sector'])
sectors_df['Country'] = np.where(sectors_df['Long name'].str.contains('EMERGING'), 'EMERGING_MARKETS', sectors_df['Country'])
sectors_df['Sector'] = np.where(sectors_df['Long name'].str.contains('COMMODIT'), 'COMMODITIES', sectors_df['Sector'])
sectors_df['Country'] = np.where(sectors_df['Long name'].str.contains('RUSSEL'), 'US', sectors_df['Country'])
sectors_df['Country'] = np.where(sectors_df['Long name'].str.contains('ASIA'), 'ASIA', sectors_df['Country'])
sectors_df['Sector'] = np.where(sectors_df['Long name'].str.contains('GOLD'), 'COMMODITIES', sectors_df['Sector'])
sectors_df['Country'] = np.where(sectors_df['Long name'].str.contains('DAX'), 'GERMANY', sectors_df['Country'])
sectors_df['Sector'] = np.where(sectors_df['Long name'].str.contains('AGRICULTURE'), 'COMMODITIES', sectors_df['Sector'])
sectors_df['Sector'] = np.where(sectors_df['Long name'].str.contains('TREASURY'), 'BOND', sectors_df['Sector'])
sectors_df['Sector'] = np.where(sectors_df['Long name'].str.contains('T-BILL'), 'BOND', sectors_df['Sector'])
sectors_df['Sector'] = np.where(sectors_df['Long name'].str.contains('ENERGY'), 'COMMODITIES', sectors_df['Sector'])

sector_mapping = sectors_df.set_index(sectors_df.columns[0])[sectors_df.columns[2]].to_dict()
country_mapping = sectors_df.set_index(sectors_df.columns[0])[sectors_df.columns[3]].to_dict()

sector_mapping['ZPDI.DE'] = 'Other'
country_mapping['ZPDI.DE'] = 'US'

import json

with open("sector_mapping.json", "w") as f:
    json.dump(sector_mapping, f, indent=4)

with open("country_mapping.json", "w") as f:
    json.dump(country_mapping, f, indent=4)
