import yfinance as yf
import pandas as pd
import numpy as np
from IPython.display import display
import matplotlib.pyplot as plt

# Define the portfolio tickers and their weights
portfolio_data = {
    'EXXT.DE': 0.150,
    'SML3.MU': 0.150,
    'EXH2.DE': 0.050,
    'LYPD.DE': 0.050,
    'QDVH.DE': 0.050,
    'UBUD.DE': 0.050
}

RISK_FREE_RATE = 0.0425
RISK_FREE_ASSET_WEIGHT = 0.5002158698157113

tickers = list(portfolio_data.keys())
weights = np.array(list(portfolio_data.values()))

# Download prices for the specified period (2025)
# Note: As 2025 is in the future, this will likely return an empty DataFrame
print(f"Attempting to download prices for {tickers} for 2025...")
try:
    prices_2025 = yf.download(tickers, start="2025-01-01", end="2026-01-01", auto_adjust=True)["Close"]
except Exception as e:
    print(f"An error occurred during download: {e}")
    prices_2025 = pd.DataFrame() # Create an empty DataFrame on error

if prices_2025.empty:
    print("No price data downloaded. This is expected as 2025 is in the future.")
    print("Please run this code with a historical date range to see actual results.")
else:
    print("Successfully downloaded data (though it might be empty if 2025 is future).")
    display(prices_2025.head())

TRADING_DAYS = 252
daily_risk_free_rate = (1 + RISK_FREE_RATE) ** (1 / TRADING_DAYS) - 1

if not prices_2025.empty:
    downloaded_tickers = prices_2025.columns.tolist()
    available_portfolio_data = {t: w for t, w in portfolio_data.items() if t in downloaded_tickers}

    if not available_portfolio_data:
        print("No matching tickers found in the downloaded data.")
    else:
        available_tickers_in_order = list(available_portfolio_data.keys())
        available_weights_in_order = np.array(
            [available_portfolio_data[t] for t in available_tickers_in_order]
        )

        # Normalize risky weights
        available_weights_in_order = (
            available_weights_in_order / np.sum(available_weights_in_order)
        )

        # Scale risky part to (1 - risk free weight)
        risky_portfolio_weight = 1 - RISK_FREE_ASSET_WEIGHT
        available_weights_in_order *= risky_portfolio_weight

        # Calculate daily returns for risky assets
        daily_returns = prices_2025[available_tickers_in_order].pct_change().dropna()

        # Risky portfolio daily return
        risky_portfolio_daily_returns = (
            daily_returns * available_weights_in_order
        ).sum(axis=1)

        # Add constant risk-free daily return
        portfolio_daily_returns = (
            risky_portfolio_daily_returns
            + RISK_FREE_ASSET_WEIGHT * daily_risk_free_rate
        )

        # Cumulative return
        cumulative_returns = (1 + portfolio_daily_returns).cumprod() - 1

        print("\nPortfolio Performance Including Risk-Free Asset:")
        if not cumulative_returns.empty:
            print(f"Total Return for 2025: {cumulative_returns.iloc[-1]:.2%}")
            display(cumulative_returns.plot(title='Total Portfolio Cumulative Returns').figure)
            plt.plot(cumulative_returns)
            plt.show()
        else:
            print("Not enough data to calculate portfolio returns.")
else:
    print("Cannot calculate portfolio performance as no price data was downloaded.")