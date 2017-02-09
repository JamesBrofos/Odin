import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter
from matplotlib import cm
from ..utilities.params import Directions
from .compute_drawdowns import compute_drawdowns
from .compute_sharpe_ratio import compute_sharpe_ratio


class Visualizer(object):
    """Fund Performance Visualizer Class

    This visualizer object is intended to provide access to a number of
    plotting utilities for visualizing the performance of the constituent
    portfolios of a fund. Support is provided for basic plots, such as the
    equity curve and drawdowns, as well as more specialized plots such as the
    rolling Sharpe ratio of the portfolios and month-over-month performance
    summaries.
    """
    def long_short_equity(self, fund, ax=None):
        if ax is None:
            ax = plt.gca()

        for i, p in enumerate(fund.fund_handler.portfolios):
            states = p.history.states
            dates = list(states.keys())
            columns = ("long", "short", "ratio")
            equity = pd.DataFrame(index=dates, columns=columns)
            for d in dates:
                filled = states[d].filled_positions
                equity.ix[d, "long"] = np.sum([
                    f.relative_value for f in filled.values()
                    if f.direction == Directions.long_dir
                ])
                equity.ix[d, "short"] = np.sum([
                    f.relative_value for f in filled.values()
                    if f.direction == Directions.short_dir
                ])
                equity["ratio"] = equity["long"] / (equity["long"] + equity["short"])

            for v in ("long", "short"):
                ax.plot(
                    equity.index, equity[v], lw=2.,
                    label="_".join((p.portfolio_handler.portfolio_id, v))
                )

        ax.set_xlabel("Date", fontsize=15.)
        ax.set_ylabel("Long / Short Equity", fontsize=15.)
        ax.legend(loc="upper left")
        ax.grid(True)

        return ax

    def rolling_sharpe(self, window, fund, ax=None):
        if ax is None:
            ax = plt.gca()

        for i, p in enumerate(fund.fund_handler.portfolios):
            rets = p.history.returns.rolling(window=window)
            rs = compute_sharpe_ratio(rets)
            ax.plot(
                rs.index, rs, lw=2.,
                label=p.portfolio_handler.portfolio_id.title()
            )

        ax.set_xlabel("Date", fontsize=15.)
        ax.set_ylabel(
            "Rolling Sharpe Ratio ({})".format(window), fontsize=15.
        )
        ax.legend(loc="upper left")
        ax.grid(True)

        return ax

    def equity(self, fund, ax=None):
        if ax is None:
            ax = plt.gca()

        for i, p in enumerate(fund.fund_handler.portfolios):
            ax.plot(
                p.history.equity.index, p.history.equity, lw=2.,
                label=p.portfolio_handler.portfolio_id.title()
            )
            ax.grid()

        ax.set_xlabel("Date", fontsize=15.)
        ax.set_ylabel("Equity", fontsize=15.)
        ax.legend(loc="upper left")
        ax.grid(True)

        return ax

    def positions(self, fund, ax=None):
        if ax is None:
            ax = plt.gca()

        for i, p in enumerate(fund.fund_handler.portfolios):
            ax.plot(
                p.history.n_positions.index, p.history.n_positions, lw=2.,
                label=p.portfolio_handler.portfolio_id.title()
            )
            ax.grid()

        ax.set_xlabel("Date", fontsize=15.)
        ax.set_ylabel("Number of Positions", fontsize=15.)
        ax.legend(loc="upper left")
        ax.grid(True)

        return ax

    def drawdown_percentage(self, fund, ax=None):
        if ax is None:
            ax = plt.gca()

        for i, p in enumerate(fund.fund_handler.portfolios):
            dd, dur = compute_drawdowns(p.history.equity, False)
            ax.plot(
                dd.index, dd, lw=2.,
                label=p.portfolio_handler.portfolio_id.title()
            )
            ax.grid()

        ax.set_xlabel("Date", fontsize=15.)
        ax.set_ylabel("Drawdown Percentage", fontsize=15.)
        ax.legend(loc="upper left")
        ax.grid(True)

        return ax

    def drawdown_duration(self, fund, ax=None):
        if ax is None:
            ax = plt.gca()

        for i, p in enumerate(fund.fund_handler.portfolios):
            dd, dur = compute_drawdowns(p.history.equity, False)
            ax.plot(
                dur.index, dur, lw=2.,
                label=p.portfolio_handler.portfolio_id.title()
            )
            ax.grid()

        ax.set_xlabel("Date", fontsize=15.)
        ax.set_ylabel("Drawdown Duration", fontsize=15.)
        ax.legend(loc="upper left")
        ax.grid(True)

        return ax

    def monthly_returns(self, fund, ax=None):
        if ax is None:
            ax = plt.gca()

        # Compute the returns on a month-over-month basis.
        history = fund.history
        monthly_ret = self.__aggregate_returns(history, 'monthly')
        monthly_ret = monthly_ret.unstack()
        monthly_ret = np.round(monthly_ret, 3)
        monthly_ret.rename(
            columns={1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr',
                     5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug',
                     9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'},
            inplace=True
        )

        # Create a heatmap showing the month-over-month returns of the portfolio
        # or the fund.
        sns.heatmap(
            monthly_ret.fillna(0) * 100.0, annot=True, fmt="0.1f",
            annot_kws={"size": 12}, alpha=1.0, center=0.0, cbar=False,
            cmap=cm.RdYlGn, ax=ax
        )
        ax.set_title('Monthly Returns (%)', fontweight='bold')
        ax.set_ylabel('')
        ax.set_yticklabels(ax.get_yticklabels(), rotation=0)
        ax.set_xlabel('')

        return ax

    def yearly_returns(self, fund, ax=None):
        if ax is None:
            ax = plt.gca()

        history = fund.history
        yearly_returns = self.__aggregate_returns(history, 'yearly') * 100.0
        yearly_returns.plot(ax=ax, kind="bar")
        ax.set_title('Yearly Returns (%)', fontweight='bold')
        ax.set_ylabel('')
        ax.set_xlabel('')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
        ax.grid(True)

        return ax

    def __aggregate_returns(self, history, aggregate="monthly"):
        cumulate_returns = lambda rets: (1. + rets).prod() - 1.

        if aggregate == "monthly":
            return history.returns.groupby(
                [lambda x: x.year, lambda x: x.month]
            ).apply(cumulate_returns)
        elif aggregate == "yearly":
            return history.returns.groupby([lambda x: x.year]).apply(
                cumulate_returns
            )
        else:
            raise ValueError(
                "Improper aggregate parameter: {}".format(aggregate)
            )

