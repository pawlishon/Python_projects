# inputes
operating_income_after_tax = 3586
net_capital_expenditures = 889
change_in_working_capital = 243
return_on_capital = 0.25
risk_free_rate = 0.0372
beta = 1.29
erp = 0.04
default_spread = 0.0075
marginal_tax_rate = 0.4
market_value = 57000
debt = 5297
number_of_years = 5
cash = 3253
management_options = 1216
future_growth = 0.03
future_cost_of_capital = 0.0676
number_of_shares = 699

fcff = operating_income_after_tax - net_capital_expenditures - change_in_working_capital
reinvestment_rate = (net_capital_expenditures + change_in_working_capital) / operating_income_after_tax
growth = reinvestment_rate * return_on_capital
cost_of_equity = risk_free_rate + beta*erp
cost_of_debt = (risk_free_rate + default_spread)*(1-marginal_tax_rate)
cost_of_capital = cost_of_equity * market_value/(debt+market_value) + cost_of_debt * debt/(debt+market_value)

reinvestment_rate_stable_growth = future_growth / future_cost_of_capital
terminal_value = operating_income_after_tax * (1 + growth)**(number_of_years) * (1 + future_growth)*(1-reinvestment_rate_stable_growth)/(future_cost_of_capital - future_growth)

operating_assets_value = 0
for year in range(number_of_years):
    if year + 1 != number_of_years:
        operating_assets_value = operating_assets_value + operating_income_after_tax * (1 + growth)**(year+1) * (
                    1 - reinvestment_rate) / ((1 + cost_of_capital) ** (year + 1))
    else:
        operating_assets_value = operating_assets_value + (operating_income_after_tax * (1 + growth) ** (year + 1) * (
                1 - reinvestment_rate) + terminal_value) / ((1 + cost_of_capital) ** (year + 1))


equity_value = operating_assets_value + cash - debt - management_options

value_per_share = equity_value / number_of_shares