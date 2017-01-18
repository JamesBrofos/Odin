import pandas as pd
from .fund import Fund
from .. import metrics


class SimulatedFund(Fund):
    """Simulated Fund Class

    The simulated fund class makes it easier to compile all of the performance
    metrics for a collection of backtested portfolios. In particular, all of the
    metrics across the individual portfolios, as well as for the fund as a
    whole, are placed into a single pandas data frame.
    """
    def __init__(
            self, data_handler, execution_handler, fund_handler,
            verbosity_level=0
    ):
        """Initialize parameters of the simulated fund object."""
        super(SimulatedFund, self).__init__(
            data_handler, execution_handler, fund_handler, 0, verbosity_level
        )

    def performance_summary(self):
        """Construct performance summaries for each of the strategies utilized
        in the simulated fund as well as the aggregation of the individual
        portfolios (i.e. the performance summary of the fund). This allows us to
        compare and contrast the drawdowns, the Sharpe ratios, and the returns
        for individual portfolios and the fund.
        """
        # Initialize data frames for the metrics of the portfolios and the fund
        # and the equity and number of positions on a day-by-day basis.
        m = pd.DataFrame()
        self.history = pd.DataFrame(
            index=self.fund_handler.portfolios[0].history.data.keys(),
            columns=["equity", "n_positions"]
        ).fillna(0.0)

        # Append the performance summary of each portfolio.
        for p in self.fund_handler.portfolios:
            m = m.append(p.performance_summary())
            self.history["equity"] += p.history.equity
            self.history["n_positions"] += p.history.n_positions

        # Compute the performance of the fund as a aggregation of the individual
        # portfolios.
        self.history["returns"] = self.history["equity"].pct_change()
        m = m.append(metrics.performance_summary(
            self.history, self.fund_handler.fund_id
        ))

        return m
