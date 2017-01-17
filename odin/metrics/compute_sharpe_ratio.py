"""Sharpe Ratio Module

Create the Sharpe ratio for the strategy, based on a benchmark of zero (i.e. no
risk-free rate information); this is coincidentally the proper risk-free rate to
utilize for dollar-neutral strategies. The Sharpe ratio generally measures the
returns of a strategy relative to its historical risk; the higher this ratio,
the more heavily leveraged the strategy may be.

The Sharpe ratio is assumed to be annualized to a yearly period since there are
252 trading days in a year. For higher or lower frequency strategies, this
annualization constant may be augmented.
"""
import numpy as np


def compute_sharpe_ratio(returns, periods=252.0):
    """Computes the Sharpe ratio based on a time-series of returns.

    Parameters
    ----------
    returns: Pandas data frame.
        A Pandas data frame where the index is a time-series of dates
        corresponding to a historical period of performance of a trading
        algorithm. The values are the day-over-day percentage changes in equity.
    periods (Optional): Float.
        The annualization constant for computing the Sharpe ratio. By default,
        this corresponds to daily trades (because there are 252 trading sessions
        per year).
    """
    return np.sqrt(periods) * np.mean(returns) / np.std(returns)
