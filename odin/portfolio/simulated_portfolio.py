from .abstract_portfolio import AbstractPortfolio
from .components import PortfolioHistory
from .. import metrics


class SimulatedPortfolio(AbstractPortfolio):
    """Simulated Portfolio Class

    The simulated portfolio is a implementation of the abstract portfolio class
    specifically for historical backtesting purposes. Specifically, whenever
    historical bar data is streamed, the value of our positions in the market is
    updated using the value of the underlying asset at the end of the time
    period.

    The simulated portfolio also records the historical equity states of the
    portfolio for the purposes of computing performance metrics of a backtest.

    Parameters
    ----------
    data_handler: Object inheriting from the abstract data handler class.
        This object supplies the data to update the prices of held positions and
        provide new bar data with which to construct features.
    position_handler: Object inheriting from the abstract position handler
        class.
        The position handler determines how much of an asset to acquire or to
        relinquish when trading signals are processed into orders.
    portfolio_handler: Portfolio handler object.
        The portfolio handler keeps track of positions that are currently held
        by the portfolio as well as the current amount of equity and capital in
        the portfolio.
    """
    def __init__(self, data_handler, position_handler, portfolio_handler):
        """Initialize parameters of the simulated portfolio object."""
        super(SimulatedPortfolio, self).__init__(
            data_handler, position_handler, portfolio_handler
        )
        self.history = PortfolioHistory(self.portfolio_handler.portfolio_id)

    def process_post_events(self):
        """Implementation of abstract base class method."""
        # Update the portfolio history of positions, capital, and equity.
        date = self.data_handler.current_date
        self.history.add_state(date, self.portfolio_handler.state)

    def performance_summary(self):
        """Compute the performance summary for the portfolio over the period of
        performance. This reports common performance metrics based on the
        equity, returns, and holdings of the portfolio at each instance in the
        time-series.

        Returns
        -------
        summary: Pandas data frame object.
            A summary of the key performance parameters of the portfolio in the
            designated time period.
        """
        self.history.compute_attributes()
        return metrics.performance_summary(
            self.history, self.portfolio_handler.portfolio_id
        )
