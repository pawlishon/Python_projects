import yfinance as yf
import pandas as pd
import yahoo_fin.stock_info as si
import requests

def my_valuation(ticker):
    # Quote table
    try:
        key_attributes_quote = ['PE Ratio (TTM)', 'Beta (5Y Monthly)', '1y Target Est', 'EPS (TTM)',
                                'Previous Close', 'Market Cap']
        try:
            quote = si.get_quote_table(ticker)
            attr_results = []
            for attribute in key_attributes_quote:
                attr_results.append(quote[attribute])
            attr_results_df = pd.DataFrame([attr_results], columns=key_attributes_quote)
        except:
            attr_results_df = pd.DataFrame([['' for x in key_attributes_quote]], columns=key_attributes_quote)
        attr_results_df['Ticker'] = ticker

        # Stats table
        try:
            stats_table = si.get_stats(ticker)
            stats_table = stats_table.loc[stats_table['Attribute'].isin(['Trailing Annual Dividend Yield 3', '5 Year Average Dividend Yield', 'Payout Ratio 4', 'Revenue Per Share (ttm)', 'Total Debt/Equity (mrq)', 'Current Ratio (mrq)', 'Profit Margin']), :].transpose()
            stats_table.columns = stats_table.iloc[0, :]
            stats_table = stats_table.iloc[1, :]
            stats_table = pd.DataFrame(stats_table)
            stats_table = stats_table.transpose().reset_index(drop=True)
        except:
            stats_table = pd.DataFrame(['', '', '', '', '', '']).transpose()
            stats_table.columns = ['Trailing Annual Dividend Yield 3', '5 Year Average Dividend Yield', 'Payout Ratio 4', 'Revenue Per Share (ttm)', 'Total Debt/Equity (mrq)', 'Current Ratio (mrq)', 'Profit Margin']

        # Stats valuation
        try:
            val = si.get_stats_valuation(ticker)
            val = val.loc[val[val.columns[0]].isin(['PEG Ratio (5 yr expected)', 'Price/Book (mrq)']), :].transpose()
            val.columns = val.iloc[0, :]
            val = val.iloc[1, :]
            val = pd.DataFrame(val)
            val = val.transpose().reset_index(drop=True)
        except:
            val = pd.DataFrame(['', '']).transpose()
            val.columns = ['PEG Ratio (5 yr expected)', 'Price/Book (mrq)']
        # Analysts recommendation
        lhs_url = 'https://query2.finance.yahoo.com/v10/finance/quoteSummary/'
        rhs_url = '?formatted=true&crumb=swg7qs5y9UP&lang=en-US&region=US&' \
                  'modules=upgradeDowngradeHistory,recommendationTrend,' \
                  'financialData,earningsHistory,earningsTrend,industryTrend&' \
                  'corsDomain=finance.yahoo.com'

        url = lhs_url + ticker + rhs_url
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                                 'like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        r = requests.get(url, headers=headers)
        if not r.ok:
            recommendation = 6
        try:
            result = r.json()['quoteSummary']['result'][0]
            recommendation = result['financialData']['recommendationMean']['fmt']
        except:
            recommendation = 6
        stats_table['Recommendation'] = recommendation

        # Adding business summary
        comp_ticker = yf.Ticker(ticker)
        stats_table['Company Summary'] = comp_ticker.info['longBusinessSummary']

        # join
        horizontal_stack = pd.concat([stats_table, val, attr_results_df], axis=1)

        # Changing columns order
        cols = horizontal_stack.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        horizontal_stack = horizontal_stack[cols]
        return horizontal_stack
    except:
        a = pd.DataFrame(columns=['Ticker', 'Trailing Annual Dividend Yield 3', '5 Year Average Dividend Yield',
                                  'Payout Ratio 4', 'Revenue Per Share (ttm)', 'Total Debt/Equity (mrq)', 'Current Ratio (mrq)',
                                  'Profit Margin', 'Recommendation', 'Company Summary',
                                  'PEG Ratio (5 yr expected) 1', 'Price/Book (mrq)',
                                  'PE Ratio (TTM)',
                                  'Beta (5Y Monthly)', '1y Target Est', 'EPS (TTM)', 'Previous Close', 'Market Cap'])
        a.loc[0] = [ticker, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
        return a


def ResultJoin(my_list):
    instrument_results = pd.DataFrame()
    for ticker in my_list:
        temp = my_valuation(ticker)
        instrument_results = pd.concat([instrument_results, temp], axis=0)
    return instrument_results
