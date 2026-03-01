import cvxpy as cp
import numpy as np
import pandas as pd
from sklearn.covariance import OAS


def portfolio_qp(
        log_returns,
        mode="max_return",
        max_risk=None,  # Max portfolio standard deviation
        min_assets=None,
        target_return=None,
        max_assets=15,
        min_weight=0.05,
        risk_free_rate=0.0,
        apply_shrinkage=False,  # New parameter for covariance shrinkage
        sector_map=None,
        sector_max_weight=None,
        country_map=None,
        country_max_weight=None
):
    """
    Mean-Variance Portfolio Optimization with:
    - No short sales
    - Max number of ETFs
    - Minimum weight threshold
    - Quadratic Programming (QP) for risk (variance)
    - Includes a risk-free instrument
    - Optional covariance shrinkage

    Parameters
    ----------
    log_returns : pd.DataFrame (T, N)
    mode : str
        "max_return" or "min_risk"
    max_risk : float
        Required if mode="max_return". Max portfolio standard deviation.
    min_assets : int, optional
        Minimum number of ETFs to select.
    target_return : float
        Required if mode="min_risk". Target expected portfolio return.
    max_assets : int
        Max number of ETFs.
    min_weight : float
        Minimum weight per selected ETF (e.05 = 5%).
    risk_free_rate : float, optional
        The annualized risk-free rate of return. Defaults to 0.0.
    apply_shrinkage : bool, optional
        If True, applies Oracle Approximating Shrinkage (OAS) to the covariance matrix.
        Defaults to False.

    Returns
    -------
    dict
    """

    T, N = log_returns.shape  # N is the number of risky assets
    mu = np.mean(log_returns.values, axis=0)  # Expected returns vector for risky assets

    tickers = log_returns.columns.tolist()

    if sector_map is not None:
        sectors = list(set(sector_map.values()))
        sector_indices = {
            sector: [i for i, t in enumerate(tickers) if sector_map[t] == sector]
            for sector in sectors
        }

    if country_map is not None:
        countries = list(set(country_map.values()))
        country_indices = {
            country: [i for i, t in enumerate(tickers) if country_map[t] == country]
            for country in countries
        }

    if apply_shrinkage:
        oas = OAS()
        Sigma = oas.fit(log_returns.values).covariance_
    else:
        Sigma = log_returns.cov().values  # Covariance matrix for risky assets

    # Decision variables
    w = cp.Variable(N + 1)  # N weights for risky assets + 1 for risk-free asset
    z = cp.Variable(N, boolean=True)  # Binary variable for risky asset selection

    # Expected portfolio return (risky assets + risk-free asset)
    expected_portfolio_return = cp.sum(cp.multiply(mu, w[:-1])) + risk_free_rate * w[-1]
    # Portfolio variance (only from risky assets)
    portfolio_variance = cp.quad_form(w[:-1], cp.psd_wrap(Sigma))

    constraints = [
        cp.sum(w) == 1,  # Sum of all weights (risky + risk-free) must be 1
        w >= 0,  # No short selling for any asset (risky or risk-free)
        w[:-1] <= z,  # If risky asset i is not selected (z[i]=0), w[i] must be 0
        w[:-1] >= min_weight * z,  # Minimum weight for selected risky assets
        cp.sum(z) <= max_assets  # Max number of selected risky assets
    ]

    if min_assets is not None:
        constraints.append(cp.sum(z) >= min_assets)  # Min number of selected risky assets

    if sector_map is not None:

        for sector, indices in sector_indices.items():

            # Max weight per sector
            if sector_max_weight is not None and sector in sector_max_weight:
                constraints.append(
                    cp.sum(w[indices]) <= sector_max_weight[sector]
                )

    if country_map is not None:

        for country, indices in country_indices.items():

            # Max weight per sector
            if country_max_weight is not None and country in country_max_weight:
                constraints.append(
                    cp.sum(w[indices]) <= country_max_weight[country]
                )

    if mode == "max_return":
        if max_risk is None:
            raise ValueError("max_risk must be provided for 'max_return' mode (as standard deviation)")
        # Max_risk is standard deviation, so we compare variance to max_risk squared
        constraints.append(portfolio_variance <= max_risk ** 2)
        objective = cp.Maximize(expected_portfolio_return)

    elif mode == "min_risk":
        if target_return is None:
            raise ValueError("target_return must be provided for 'min_risk' mode")
        constraints.append(expected_portfolio_return >= target_return)
        objective = cp.Minimize(portfolio_variance)  # Minimize portfolio variance

    else:
        raise ValueError("Invalid mode. Use 'max_return' or 'min_risk'.")

    problem = cp.Problem(objective, constraints)
    # Use ECOS_BB for mixed-integer quadratic programs
    problem.solve(solver='ECOS_BB')

    if problem.status not in [cp.OPTIMAL, cp.OPTIMAL_INACCURATE]:
        print(f"Problem did not solve to optimality. Status: {problem.status}")
        return {
            "weights": None,
            "selected_assets": None,
            "num_assets": 0,
            "expected_return": None,
            "risk": None  # Risk here is standard deviation
        }

    # Calculate actual standard deviation from optimized variance
    actual_risk = np.sqrt(portfolio_variance.value)

    if sector_map is not None:
        print("\nSector Weights:")
        for sector, indices in sector_indices.items():
            sector_weight = np.sum(w.value[indices])
            if sector_weight > 1e-6:  # avoid printing tiny numerical noise
                print(f"{sector}: {sector_weight:.4f}")

    # -----------------------------------
    # Print Country Weights (risky assets only)
    # -----------------------------------
    if country_map is not None:
        print("\nCountry Weights:")
        for country, indices in country_indices.items():
            country_weight = np.sum(w.value[indices])
            if country_weight > 1e-6:
                print(f"{country}: {country_weight:.4f}")

    # The 'selected_assets' and 'num_assets' refer to risky assets only
    # The last weight in w.value corresponds to the risk-free asset
    return {
        "weights": w.value,
        "selected_assets": z.value,
        "num_assets": int(np.sum(z.value > 0.5)),
        "expected_return": expected_portfolio_return.value,
        "risk": actual_risk
    }


def portfolio_lp(
    log_returns,
    mode="max_return",
    max_risk=None,
    min_assets=None,
    target_return=None,
    max_assets=15,
    min_weight=0.05
):
    """
    MILP Portfolio Optimization with:
    - No short sales
    - Max number of ETFs
    - Minimum weight threshold
    - LP risk proxy (MAD)

    Parameters
    ----------
    log_returns : np.ndarray (T, N)
    mode : str
        "max_return" or "min_risk"
    max_risk : float
        Required if mode="max_return"
    target_return : float
        Required if mode="min_risk"
    max_assets : int
        Max number of ETFs
    min_weight : float
        Minimum weight per selected ETF (e.g. 0.05 = 5%)

    Returns
    -------
    dict
    """

    T, N = log_returns.shape
    mu = np.mean(log_returns.values, axis=0) # Explicitly use .values

    # Decision variables
    w = cp.Variable(N)
    u = cp.Variable(T)
    z = cp.Variable(N, boolean=True)

    portfolio_returns = log_returns.values @ w # Explicitly use .values
    expected_return = mu @ w
    risk = cp.sum(u) / T

    constraints = [
        cp.sum(w) == 1,
        w >= 0,
        w <= z,
        w >= min_weight * z,     # ⭐ minimum 5% per selected ETF
        cp.sum(z) <= max_assets,
        cp.sum(z) >= min_assets,
        u >= portfolio_returns - expected_return,
        u >= -(portfolio_returns - expected_return)
    ]

    if mode == "max_return":
        if max_risk is None:
            raise ValueError("max_risk must be provided")
        constraints.append(risk <= max_risk)
        objective = cp.Maximize(expected_return)

    elif mode == "min_risk":
        if target_return is None:
            raise ValueError("target_return must be provided")
        constraints.append(expected_return >= target_return)
        objective = cp.Minimize(risk)

    else:
        raise ValueError("Invalid mode")

    problem = cp.Problem(objective, constraints)
    problem.solve(solver='ECOS_BB') # Changed to ECOS_BB

    if problem.status not in [cp.OPTIMAL, cp.OPTIMAL_INACCURATE]:
        print(f"Problem did not solve to optimality. Status: {problem.status}")
        return {
            "weights": None,
            "selected_assets": None,
            "num_assets": 0,
            "expected_return": None,
            "risk": None
        }

    return {
        "weights": w.value,
        "selected_assets": z.value,
        "num_assets": int(np.sum(z.value > 0.5)),
        "expected_return": expected_return.value,
        "risk": risk.value
    }