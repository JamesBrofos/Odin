import pandas as pd
from copy import deepcopy
from collections import OrderedDict


class PortfolioHistory(object):
    """Portfolio History Class

    The portfolio history class keeps track of historical portfolio states as in
    a time-series. This is achieved by copying the state of the portfolio on a
    known date into a dictionary where the keys are dates that have been ordered
    temporally.

    This allows us to iterate over the dates in a logical order as we track
    changes in portfolio equity, positions, and capital.

    Parameters
    ----------
    portfolio_id: String.
        A unique identifier assigned to the portfolio.
    """
    def __init__(self, portfolio_id):
        """Initialize parameters of the portfolio history object."""
        self.portfolio_id = portfolio_id
        self.states = OrderedDict()

    def add_state(self, date, portfolio_state):
        """Update the dictionary of portfolio states ordered by dates by
        appending the latest entry.

        Parameters
        ----------
        date: A datetime object.
            The date at which to record the current state of the portfolio.
        portfolio_state: Portfolio state object.
            A portfolio state object which will be archived as the state of the
            portfolio on the provided date. In order to avoid memory problems, a
            copy of the state is made.
        """
        self.states[date] = deepcopy(portfolio_state)

    def compute_attributes(self):
        """Compute the historical time-series attribute curves for the
        portfolio. These curves are in particular:
            1. A historical record of the aggregate equity of the portfolio, on
               a time period by time period basis.
            2. A historical record of how many positions there were in each time
               period.
            3. The historical returns for each time period.
        """
        # Create pandas series objects for the historical equity and number of
        # positions. The series for the returns will be computed later.
        self.equity = pd.Series()
        self.n_positions = pd.Series()
        # Iterate over each time period in the ordered dictionary of portfolio
        # states.
        for date in self.states:
            state = self.states[date]
            self.n_positions.ix[date] = len(state.filled_positions)
            self.equity.ix[date] = state.equity

        # Compute the returns in each time period directly from the change in
        # portfolio equity.
        self.returns = self.equity.pct_change()
