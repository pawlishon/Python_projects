import pandas as pd
import requests
import json
import yahoo_fin.stock_info as si

# Get query table
sp500_tickers = si.tickers_sp500()
sp500_string = ','.join(sp500_tickers)
querystring = {"symbols":sp500_string}
url = "https://yfapi.net/v6/finance/quote"
headers = {
    'x-api-key': "AkPEywBHa11Qwn1Z2Mdbe9hTTSVYRACo6v8HLxM6"
    }
response = requests.request("GET", url, headers=headers, params=querystring)
data = response.text
try:
    json_acceptable_string = data.replace("'", "\"")
    result_dict = json.loads(json_acceptable_string)
except:
    result_dict = json.loads(data)
result_df = result_dict['quoteResponse']['result']

longest_dict = [len(result) for result in result_df].index(max([len(result) for result in result_df]))
res_df = pd.DataFrame(columns=list(result_df[longest_dict].keys()))
for i in range(len(result_df)):
    for col in res_df.columns:
        if col in result_df[i].keys():
            res_df.loc[i, col] = result_df[i][col]

res_df.to_excel('sp500.xlsx', header=True, index=False)


# quoteSummary
sp500_tickers = si.tickers_sp500()
for ticker in sp500_tickers[490:]:
    url_2 = 'https://yfapi.net/v11/finance/quoteSummary/' + ticker
    headers = {
        'x-api-key': "AkPEywBHa11Qwn1Z2Mdbe9hTTSVYRACo6v8HLxM6"
        }
    params={'modules': 'defaultKeyStatistics,assetProfile,earnings, earningsHistory,financialData, incomeStatementHistory, balanceSheetHistory, cashflowStatementHistory' }
    response = requests.request("GET", url_2, headers=headers, params=params)
    data = response.text
    result_dict = json.loads(data)
    with open(f'{ticker}.json', 'w') as fp:
        json.dump(result_dict['quoteSummary']['result'][0], fp)

