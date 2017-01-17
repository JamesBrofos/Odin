from .abstract_position_handler import AbstractPositionHandler
from ...utilities.params import PriceFields
from ...utilities.finance import modern_portfolio_solve


class ModernPortfolioPositionHandler(AbstractPositionHandler):
    """Modern Portfolio Theory Position Handler Class

    """
    def __init__(self, data_handler, omega=1.0):
        """Initialize parameters of the modern portfolio position handler
        object.
        """
        super(ModernPortfolioPositionHandler, self).__init__()
        self.data_handler = data_handler
        self.omega = omega

    def buy_size_order(self, symbol, portfolio_handler):
        """Implementation of abstract base class method."""
        # Get the current amount of spendable capital as well as the current
        # amount of equity in the portfolio.
        capital, equity = portfolio_handler.capital, portfolio_handler.equity
        # Compute the weights for each asset for which we have bars.
        bars = portfolio_handler.data_handler.bars["adj_price_close"]
        series = modern_portfolio_solve(bars, self.omega)

        try:
            spend = min(equity * series[symbol], capital)
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
        return portfolio_handler.positions[symbol].quantity
