from .abstract_position_handler import AbstractPositionHandler
from ...utilities.params import PriceFields


class FixedQuantityPositionHandler(AbstractPositionHandler):
    """Fixed Quantity Position Handler Class

    The fixed position handler object will compute position sizes to be a
    user-specified constant, regardless of equity. This results in all holdings
    consisting of equal numbers of shares, though these positions are likely to
    represent wildly different amounts of equity. This position handler
    corresponds to buying a single lot of shares.
    """
    def __init__(self, default_buy_size, default_sell_size):
        """Initialize parameters of the fixed quantity position handler object.
        """
        super(FixedPositionHandler, self).__init__()
        self.default_buy_size = default_buy_size
        self.default_sell_size = default_sell_size

    def buy_size_order(self, symbol, portfolio_state):
        """Implementation of abstract base class method."""
        return self.default_buy_size

    def sell_size_order(self, symbol, portfolio_state):
        """Implementation of abstract base class method."""
        return self.default_sell_size


class FixedWeightPositionHandler(AbstractPositionHandler):
    """Fixed Weight Position Handler Class
    """
    def __init__(self, weights, data_handler):
        """Initialize parameters of the fixed weight position handler object.
        """
        super(FixedWeightPositionHandler, self).__init__()
        self.weights = weights
        self.data_handler = data_handler

    def buy_size_order(self, symbol, portfolio_handler):
        """Implementation of abstract base class method."""
        # Get the current amount of spendable capital as well as the current
        # amount of equity in the portfolio.
        capital, equity = portfolio_handler.capital, portfolio_handler.equity
        # Compute the amount that should be spent on this position as well as an
        # estimate of the cost of an individual share of the underlying asset.
        spend = min(equity * self.weights[symbol], capital)

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
