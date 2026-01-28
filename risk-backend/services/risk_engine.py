import numpy as np
import pandas as pd
from scipy.stats import norm


def compute_risk(prices: list, risk_free_rate: float = 0.03):
    if len(prices) < 2:
        return {"error": "Not enough data for risk analysis"}

    # Convert to Pandas Series
    prices = pd.Series(prices)

    # Calculate daily returns
    returns = prices.pct_change().dropna()

    # Annualized volatility
    volatility = returns.std() * np.sqrt(252)

    # Average daily return → Annualized
    avg_return = returns.mean() * 252

    # Sharpe Ratio
    sharpe_ratio = (avg_return - risk_free_rate) / volatility if volatility != 0 else None

    # Value at Risk (95% confidence), parametric Gaussian
    z_score = norm.ppf(0.95)
    var_95 = (returns.mean() - z_score * returns.std())

    return {
        "volatility": float(volatility),
        "sharpe_ratio": float(sharpe_ratio) if sharpe_ratio else None,
        "var_95": float(var_95),
        "avg_return": float(avg_return),
    }
