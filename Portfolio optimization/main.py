# prices.to_excel('ETF_data_revolut.xlsx')
import pandas as pd
import numpy as np
from portfolio_optimizers import portfolio_qp
import json

MODE = 'min_risk' # 'min_risk', 'max_return'
TARGET_YR_RETURN = 0.10
MAX_YR_RISK = 0.07
RISK_FREE_RATE = 0.0425
APPLY_COVARIANCE_SHRINKAGE = True
NR_OF_YRS_HISTORIC_DATA =10
SECTOR_MAX_WEIGHT = 0.20
COUNTRY_MAX_WEIGHT = 0.20
TECHNOLOGY_SECTOR_MAX_WEIGHT_OVERRIDE = 0.15

prices = pd.read_excel('ETF_data_revolut.xlsx')
prices.set_index('Date', inplace=True)
prices.head()

with open("sector_mapping.json", "r") as f:
    sector_mapping = json.load(f)
with open("country_mapping.json", "r") as f:
    country_mapping = json.load(f)

sector_max_assets = {sector: SECTOR_MAX_WEIGHT for sector in set(sector_mapping.values())}
country_max_assets = {country: COUNTRY_MAX_WEIGHT for country in set(country_mapping.values())}
if TECHNOLOGY_SECTOR_MAX_WEIGHT_OVERRIDE is not None:
    sector_max_assets['TECHNOLOGY'] = TECHNOLOGY_SECTOR_MAX_WEIGHT_OVERRIDE

# Drop columns that are entirely NaN
prices = prices.dropna(axis=1, how="all")

# Forward-fill short gaps (holidays)
prices = prices.ffill()

weekly_prices = prices.resample("W-FRI").last()
weekly_log_returns = np.log(weekly_prices / weekly_prices.shift(1))
sample_input = weekly_log_returns.copy()#.sample(n=300, axis=1)

if NR_OF_YRS_HISTORIC_DATA < 10:
    import pandas as pd

    # Get the last date in the sample_input
    last_date = sample_input.index.max()

    # Calculate the date 3 years prior
    start_date_last_3_years = last_date - pd.DateOffset(years=NR_OF_YRS_HISTORIC_DATA)

    # Filter sample_input for the last 3 years
    sample_input = sample_input[sample_input.index >= start_date_last_3_years]

# Keeping only ETFs with at least 80 % of returns in this period
MIN_OBSERVATIONS = int(0.8 * 52 * NR_OF_YRS_HISTORIC_DATA)

valid_assets = sample_input.count() >= MIN_OBSERVATIONS
sample_input = sample_input.loc[:, valid_assets]

# Replace NaN only BEFORE asset inception with 0
sample_input = sample_input.apply(
    lambda col: col.fillna(0) if col.first_valid_index() is not None else col,
    axis=0
)

# Cross sectional mean for the rest
sample_input = sample_input.apply(
    lambda row: row.fillna(row.mean()),
    axis=1
)

if MODE == 'max_return':
    res_max = portfolio_qp(
        sample_input, # .fillna(0), # Fill NaN values with 0 before optimization
        mode="max_return",
        max_risk=MAX_YR_RISK / np.sqrt(52), # Converted from annualized 10% to weekly
        max_assets=15,
        min_assets=5,
        min_weight=0.05,
        risk_free_rate=RISK_FREE_RATE /52,
        apply_shrinkage=APPLY_COVARIANCE_SHRINKAGE,
        sector_map=sector_mapping,
        country_map=country_mapping,
        sector_max_weight=sector_max_assets,
        country_max_weight=country_max_assets
    )

    print("ETFs used:", res_max["num_assets"])

    selected_indices = np.where(res_max['selected_assets'] > 0.5)[0]
    solution_tickers = sample_input.columns[selected_indices].tolist()
    solution_weights = res_max['weights'][selected_indices]

    print("Tickers in the optimal portfolio:")
    for ticker, weight in zip(solution_tickers, solution_weights):
        print(f"- {ticker}: {weight:.3f}")

    print(res_max['risk'] * np.sqrt(52))
    print(res_max['expected_return'] * 52)
elif MODE == 'min_risk':
    res_min = portfolio_qp(
        sample_input, #.fillna(0), # Fill NaN values with 0 before optimization
        mode="min_risk",
        target_return=TARGET_YR_RETURN / 52, # Converted from annualized 10% to weekly
        max_assets=15,
        min_assets=5,
        min_weight=0.05,
        risk_free_rate=RISK_FREE_RATE/52,
        apply_shrinkage=APPLY_COVARIANCE_SHRINKAGE,
        sector_map=sector_mapping,
        country_map=country_mapping,
        sector_max_weight=sector_max_assets,
        country_max_weight=country_max_assets
    )
    print("ETFs used:", res_min["num_assets"])

    selected_indices = np.where(res_min['selected_assets'] > 0.5)[0]
    solution_tickers = sample_input.columns[selected_indices].tolist()
    solution_weights = res_min['weights'][selected_indices]

    print("Tickers in the optimal portfolio:")
    for ticker, weight in zip(solution_tickers, solution_weights):
        print(f"- {ticker}: {weight:.3f}")

    print(f"Invested in RF asset: {res_min['weights'][-1]}")
    print(f"Portfolio risk: {res_min['risk'] * np.sqrt(52)}")
    print(f"Portfolio return: {res_min['expected_return'] * 52}")