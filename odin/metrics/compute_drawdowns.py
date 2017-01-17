"""Drawdowns Module

Calculate the largest peak-to-trough drawdown of the profit-and-loss curve as
well as the duration of the drawdown. This function requires that the equity
curve is represented by a pandas series object. Drawdowns measure simultaneously
the maximum amount of capital that has been lost in the course of a strategy in
addition to the amount of time elapsed since the strategy was able to recover
from losses. As a rule of thumb, strategies with large (more than ten percent)
or lengthy (more than four months) drawdowns will not have large Sharpe ratios.
"""
import pandas as pd


def compute_drawdowns(equity_curve, return_max=True):
    """Computes the drawdown time-series for a provided equity curve. Returns
    both the drawdowns and their durations (or the maximums thereof).

    Parameters
    ----------
    equity_curve: Pandas data frame.
        A Pandas data frame whose index is a time series of dates corresponding
        to trading days over the course of a historical time period.
    return_max (Optional): Boolean.
        A boolean indicator for whether or not the time series of the drawdown
        is returned or if only the maximums for the series should be returned.
    """
    # Calculate the cumulative returns curve and set up the high water mark.
    # Then create the drawdown and duration series.
    hwm = equity_curve.cummax()
    drawdown = (hwm - equity_curve) / hwm
    eq_idx = equity_curve.index
    duration = pd.Series(index=eq_idx)

    # Loop over the index range.
    for date_ind in range(len(eq_idx)):
        duration.ix[date_ind] = (
            0 if drawdown.ix[date_ind] == 0
            else duration.ix[date_ind - 1] + 1
        )

    if return_max:
        return drawdown.max(), duration.max()
    else:
        return drawdown, duration
