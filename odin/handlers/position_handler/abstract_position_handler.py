from abc import ABCMeta, abstractmethod
from ...utilities.params import TradeTypes, PriceFields


class AbstractPositionHandler(object):
    """Abstract Position Handler Class

    The abstract position handler class determines the size of the order to
    place according to a specified criterion.
    """
    __metaclass__ = ABCMeta

    def __init__(self, data_handler):
        """Initialize parameters of the abstract position handler object."""
        self.order_sizer = {
            TradeTypes.buy_trade: self.buy_size_order,
            TradeTypes.sell_trade: self.sell_size_order,
            TradeTypes.exit_trade: self.exit_size_order
        }
        self.data_handler = data_handler

    @abstractmethod
    def compute_buy_weights(self, signal_event, portfolio_handler):
        """Compute the proportion of equity to spend on the provided signal
        event when buying into a position.
        """
        raise NotImplementedError()

    @abstractmethod
    def compute_sell_weights(self, signal_event, portfolio_handler):
        """Compute the proportion of equity to spend on the provided signal
        event when selling out of a position.
        """
        raise NotImplementedError()

    def buy_size_order(self, signal_event, portfolio_handler):
        """This method will be called to determine the number of shares that
        should be bought into when entering a long or short position.
        """
        # Get the current amount of spendable capital as well as the current
        # amount of equity in the portfolio.
        capital, equity = portfolio_handler.capital, portfolio_handler.equity
        # Compute the amount that should be spent on this position as well as an
        # estimate of the cost of an individual share of the underlying asset.
        symbol = signal_event.symbol
        weights = self.compute_buy_weights(signal_event, portfolio_handler)
        spend = min(equity * weights[symbol], capital)

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

    def sell_size_order(self, signal_event, portfolio_handler):
        """This method determines the number of shares to liquidate when selling
        a position.
        """
        symbol = signal_event.symbol
        weights = self.compute_sell_weights(signal_event, portfolio_handler)
        pos = portfolio_handler.filled_positions[symbol]
        return int(weights[symbol] * pos.quantity)

    def exit_size_order(self, signal_event, portfolio_handler):
        """This method liquidates the entire position."""
        symbol = signal_event.symbol
        try:
            val = portfolio_handler.filled_positions[symbol].quantity
        except KeyError:
            val = 0
        finally:
            return val
