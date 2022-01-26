import pandas as pd
import yahoo_fin.stock_info as si
import warnings
warnings.filterwarnings('ignore')

def get_financial_statements(ticker):

    income_statement = si.get_income_statement(ticker)
    balance_sheet = si.get_balance_sheet(ticker)
    cash_flow= si.get_cash_flow(ticker)

    is_valid_pos = ['totalRevenue', 'costOfRevenue', 'grossProfit', 'sellingGeneralAdministrative', 'researchDevelopment',
                    'operatingIncome', 'incomeBeforeTax', 'netIncome', 'interestExpense']

    bs_valid_pos = ['totalLiab', 'totalStockholderEquity', 'totalAssets', 'cash', 'shortTermInvestments', 'netReceivables',
                    'inventory', 'otherCurrentAssets', 'totalCurrentAssets', 'propertyPlantEquipment', 'accountPayable',
                    'totalCurrentLiabilities', 'netTangibleAssets', 'commonStock', 'retainedEarnings', 'treasuryStock',
                    'longTermDebt', 'shortLongTermDebt']

    cs_valid_pos = ['capitalExpenditures', 'issuanceOfStock', 'repurchaseOfStock', 'depreciation']

    income_statement_valid = income_statement[income_statement.index.isin(is_valid_pos)]
    balance_sheet_valid = balance_sheet[balance_sheet.index.isin(bs_valid_pos)]
    cash_flow_valid = cash_flow[cash_flow.index.isin(cs_valid_pos)]


    income_statement_valid.loc['grossProfitMargin'] = income_statement_valid.loc['grossProfit'] / income_statement_valid.loc['totalRevenue']
    income_statement_valid.loc['grossProfitMargin'] = income_statement_valid.loc['grossProfitMargin'].apply(lambda x: round(x, 4))
    income_statement_valid.loc['taxPaid'] = (income_statement_valid.loc['incomeBeforeTax'] - income_statement_valid.loc['netIncome']) / income_statement_valid.loc['incomeBeforeTax']
    income_statement_valid.loc['taxPaid'] = income_statement_valid.loc['taxPaid'].apply(lambda x: round(x, 4))
    income_statement_valid.loc['interestExpense'] = income_statement_valid.loc['interestExpense'] / income_statement_valid.loc['operatingIncome']
    income_statement_valid.loc['interestExpense'] = income_statement_valid.loc['interestExpense'].apply(lambda x: round(x, 4))
    income_statement_valid.loc['netRatio'] = income_statement_valid.loc['netIncome'] / income_statement_valid.loc['totalRevenue']
    income_statement_valid.loc['netRatio'] = income_statement_valid.loc['netRatio'].apply(lambda x: round(x, 4))
    income_statement_valid.loc['sellingGeneralAdministrative'] = income_statement_valid.loc['sellingGeneralAdministrative'] / income_statement_valid.loc['grossProfit']
    income_statement_valid.loc['sellingGeneralAdministrative'] = income_statement_valid.loc['sellingGeneralAdministrative'].apply(lambda x: round(x, 4))
    income_statement_valid.loc['researchDevelopment'] = income_statement_valid.loc['researchDevelopment'] / income_statement_valid.loc['grossProfit']
    income_statement_valid.loc['researchDevelopment'] = income_statement_valid.loc['researchDevelopment'].apply(lambda x: round(x, 4))

    balance_sheet_valid.loc['currentRatio'] = balance_sheet_valid.loc['totalCurrentLiabilities'] / balance_sheet_valid.loc['totalCurrentAssets']
    balance_sheet_valid.loc['currentRatio'] = balance_sheet_valid.loc['currentRatio'].apply(lambda x: round(x, 4))
    balance_sheet_valid.loc['debtToESRatio'] = balance_sheet_valid.loc['totalLiab'] / balance_sheet_valid.loc['totalStockholderEquity']
    balance_sheet_valid.loc['debtToESRatio'] = balance_sheet_valid.loc['debtToESRatio'].apply(lambda x: round(x,4))
    balance_sheet_valid.loc['longOverShortDebt'] = balance_sheet_valid.loc['longTermDebt'] > balance_sheet_valid.loc['shortLongTermDebt']

    master_table = pd.concat([income_statement_valid, balance_sheet_valid, cash_flow_valid])
    master_table.loc['returnOnShareholdersEquity'] = master_table.loc['netIncome'] / master_table.loc['totalStockholderEquity']
    master_table.loc['returnOnShareholdersEquity'] = master_table.loc['returnOnShareholdersEquity'].apply(lambda x: round(x, 4))
    master_table.loc['depreciation'] = master_table.loc['depreciation'] / master_table.loc['grossProfit']
    master_table.loc['depreciation'] = master_table.loc['depreciation'].apply(lambda x: round(x,4))
    cols=[]
    for col in master_table.columns:
        cols.append(col.strftime('%d-%m-%Y'))
    master_table.columns= cols
    master_table = master_table.reset_index()
    return master_table