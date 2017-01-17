from ...utilities.mixins import EquityMixin


class PortfolioState(EquityMixin):
    """Portfolio State Class

    The portfolio state objects captures all the elements of the portfolio at a
    particular instance in time. In particular, it aggregates the current free
    capital of the portfolio as well as all of the positions that are presently
    held.

    The equity of the portfolio is computed directly from the specified capital
    and the current value of the positions.

    Parameters
    ----------
    capital: Float.
        The amount of capital (measured in USD) presently held by the portfolio.
    filled_positions: Dictionary.
        A dictionary of filled position objects mapping symbols to the
        corresponding fill representation.
    maximum_capacity: Integer.
        An integer representing the maximum number of filled  positions that can
        be held by a portfolio at any given time.
    symbols: List.
        A list of symbols for which the data handler associated with the
        portfolio streamed bar data.
    portfolio_id: String.
        A unique identifier assigned to the portfolio.
    """
    def __init__(
            self, capital, filled_positions, maximum_capacity, portfolio_id
    ):
        """Initialize parameters of the portfolio state object."""
        self.capital = capital
        self.filled_positions = filled_positions
        self.maximum_capacity = maximum_capacity
        self.portfolio_id = portfolio_id

    def __str__(self):
        """String representation of the portfolio state object.

        This representation is used generally for making a human-readable text
        of the status of the portfolio at a given time.
        """
        buf = "-" * 46 + "\n"
        head = "\n" + "=" * (len(buf) - 1) + "\n"
        s = head + "Portfolio:\t" + self.portfolio_id + "\n"
        s += buf + "Equity:\t\t{:0.2f}\nCapital:\t{:0.2f}\n".format(
            self.equity, self.capital
        )
        s += buf
        for pos in self.filled_positions.values():
            s += str(pos) + "\n"
        s += buf

        return s
