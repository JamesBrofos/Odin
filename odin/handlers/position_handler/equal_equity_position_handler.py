import numpy as np
from .abstract_position_handler import AbstractPositionHandler
from ...utilities.params import PriceFields


class EqualEquityPositionHandler(AbstractPositionHandler):
    """Equal Equity Position Handler Class

    The equal equity position handler class acknowledges that a particular
    amount of equity exists in the portfolio and that there is a desire to
    spread that equity equally amount a fixed number of assets. This allows
    every position to represent approximately the same amount of equity, but
    with different numbers of shares held in each.
    """
    def __init__(self, n_positions, data_handler):
        """Initialize parameters of the equal equity position handler object."""
        super(EqualEquityPositionHandler, self).__init__()
        self.n_positions = n_positions
        self.data_handler = data_handler

    def buy_size_order(self, symbol, portfolio_handler):
        """Implementation of abstract base class method."""
        # Get the current amount of spendable capital as well as the current
        # amount of equity in the portfolio.
        capital, equity = portfolio_handler.capital, portfolio_handler.equity
        # Compute the amount that should be spent on this position as well as an
        # estimate of the cost of an individual share of the underlying asset.
        spend = min(equity / self.n_positions, capital)

        try:
            cost = self.data_handler.prices.ix[
                PriceFields.current_price.value, 0, symbol
            ]
        except KeyError:
            # If we can't find a cost of the asset, then don't try to buy any.
            return 0
        else:
            # Compute the number of shares.
            return max(int(spend / cost), 0)

    def sell_size_order(self, symbol, portfolio_handler):
        """Implementation of abstract base class method."""
        return portfolio_handler.filled_positions[symbol].quantity
