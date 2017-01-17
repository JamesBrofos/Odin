import pandas as pd
from .compute_drawdowns import compute_drawdowns
from .compute_sharpe_ratio import compute_sharpe_ratio


def performance_summary(history, portfolio_id):
    """This function computes common performance metrics for a time-series of
    portfolio equity states. For instance, the function will compute the Sharpe
    ratio, the maximum drawdown, the drawdown duration, the annualized returns
    and the average number of positions held at each moment in the time-series.

    Parameters
    ----------
    history: A portfolio history object.
        The portfolio history object containing the equity and positional
        information for a time-series corresponding to the period of performance
        of a trading algorithm.
    portfolio_id: String.
        A unique identifier assigned to the portfolio.
    """
    equity = history.equity
    n = len(equity)
    m = pd.DataFrame(index=[portfolio_id])
    m.ix[portfolio_id, "total equity"] = equity.ix[-1]
    m.ix[portfolio_id, "max equity"] = equity.max()
    m.ix[portfolio_id, "max drawdown"], m.ix[portfolio_id, "max duration"] = (
        compute_drawdowns(equity)
    )
    m.ix[portfolio_id, "sharpe ratio"] = (
        compute_sharpe_ratio(history.returns)
    )
    m.ix[portfolio_id, "avg positions"] = history.n_positions.mean()
    m.ix[portfolio_id, "annualized returns"] = (
        (1. + history.returns).prod() ** (252. / n)
    )

    return m
