import mysql.connector
import json
import os

cnx = mysql.connector.connect(user='admin', password='admin',
                              host='ZZZ',
                              database='STOCKS')


def get_value(object, key):
    try:
        return object[key]['raw']
    except KeyError:
        return 'NULL'


# Filling default key statistics table

for file in os.listdir('QuoteSummaries'):
    try:
        curs = cnx.cursor()
        f = open(f'QuoteSummaries/{file}')
        a = json.load(f)
        ticker = '"' + file.split('.')[0] + '"'
        defaultKKeyStatistics = a['defaultKeyStatistics']

        result_dict = {'ticker': ticker,
                       'enterpriseValue': get_value(defaultKKeyStatistics, 'enterpriseValue'),
                       'forwardPE': get_value(defaultKKeyStatistics, 'forwardPE'),
                       'profitMargins': get_value(defaultKKeyStatistics, 'profitMargins'),
                       'sharesOutstanding': get_value(defaultKKeyStatistics, 'sharesOutstanding'),
                       'shortRatio': get_value(defaultKKeyStatistics, 'shortRatio'),
                       'beta': get_value(defaultKKeyStatistics, 'beta'),
                       'morningStarOverallRating': get_value(defaultKKeyStatistics, 'morningStarOverallRating'),
                       'bookValue': get_value(defaultKKeyStatistics, 'bookValue'),
                       'priceToBook': get_value(defaultKKeyStatistics, 'priceToBook'),
                       'ytdReturn': get_value(defaultKKeyStatistics, 'ytdReturn'),
                       'beta3Year': get_value(defaultKKeyStatistics, 'beta3Year'),
                       'threeYearAverageReturn': get_value(defaultKKeyStatistics, 'threeYearAverageReturn'),
                       'fiveYearAverageReturn': get_value(defaultKKeyStatistics, 'fiveYearAverageReturn'),
                       'priceToSalesTrailing12Months': get_value(defaultKKeyStatistics, 'priceToSalesTrailing12Months'),
                       'trailingEps': get_value(defaultKKeyStatistics, 'trailingEps'),
                       'forwardEps': get_value(defaultKKeyStatistics, 'forwardEps'),
                       'pegRatio': get_value(defaultKKeyStatistics, 'pegRatio'),
                       'enterpriseToRevenue': get_value(defaultKKeyStatistics, 'enterpriseToRevenue'),
                       'enterpriseToEbitda': get_value(defaultKKeyStatistics, 'enterpriseToEbitda')
                       }

        insert = [str(item) for item in list(result_dict.values()) + ['NULL']]
        query = "insert into STOCKS.default_key_statistics values (" + ', '.join(insert) + ")"
        curs.execute(query)
        cnx.commit()
        print(f'Script inserted data for file {file}')
    except:
        print(f'Script failed for file {file}')


# Filling financial data table
for file in os.listdir('QuoteSummaries'):
    try:
        curs = cnx.cursor()
        f = open(f'QuoteSummaries/{file}')
        a = json.load(f)
        ticker = '"' + file.split('.')[0] + '"'
        financialData = a['financialData']

        result_dict = {'ticker': ticker,
                       'currentPrice': get_value(financialData, 'currentPrice'),
                       'totalCash': get_value(financialData, 'totalCash'),
                       'totalCashPerShare': get_value(financialData, 'totalCashPerShare'),
                       'ebitda': get_value(financialData, 'ebitda'),
                       'totalDebt': get_value(financialData, 'totalDebt'),
                       'quickRatio': get_value(financialData, 'quickRatio'),
                       'currentRatio': get_value(financialData, 'currentRatio'),
                       'totalRevenue': get_value(financialData, 'totalRevenue'),
                       'debtToEquity': get_value(financialData, 'debtToEquity'),
                       'revenuePerShare': get_value(financialData, 'revenuePerShare'),
                       'returnOnAssets': get_value(financialData, 'returnOnAssets'),
                       'returnOnEquity': get_value(financialData, 'returnOnEquity'),
                       'grossProfits': get_value(financialData, 'grossProfits'),
                       'freeCashflow': get_value(financialData, 'freeCashflow'),
                       'operatingCashflow': get_value(financialData, 'operatingCashflow'),
                       'earningsGrowth': get_value(financialData, 'earningsGrowth'),
                       'revenueGrowth': get_value(financialData, 'revenueGrowth'),
                       'grossMargins': get_value(financialData, 'grossMargins'),
                       'ebitdaMargins': get_value(financialData, 'ebitdaMargins'),
                       'operatingMargins': get_value(financialData, 'operatingMargins'),
                       'profitMargins': get_value(financialData, 'profitMargins')
                       }

        insert = [str(item) for item in list(result_dict.values()) + ['NULL']]
        query = "insert into STOCKS.financial_data values (" + ', '.join(insert) + ")"
        curs.execute(query)
        cnx.commit()
        print(f'Script inserted data for file {file}')
    except:
        print(f'Script failed for file {file}')


# Earnings and revenue

for file in os.listdir('QuoteSummaries'):
    try:
        curs = cnx.cursor()
        f = open(f'QuoteSummaries/{file}')
        a = json.load(f)
        ticker = '"' + file.split('.')[0] + '"'
        earnings = a['earnings']['financialsChart']['yearly']
        for record in earnings:
            result_dict = {'ticker': ticker,
                           'date': record['date'],
                           'revenue': get_value(record, 'revenue'),
                           'earnings': get_value(record, 'earnings')
                           }
            insert = [str(item) for item in list(result_dict.values())]
            query = "insert into STOCKS.earnings values (" + ', '.join(insert) + ")"
            curs.execute(query)
            cnx.commit()
            print(f"Script inserted data for file {file} and year {record['date']}")
    except:
        print(f'Script failed for file {file}')