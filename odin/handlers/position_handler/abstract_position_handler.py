from abc import ABCMeta, abstractmethod
from ...utilities.params import TradeTypes


class AbstractPositionHandler(object):
    """Abstract Position Handler Class

    The abstract position handler class determines the size of the order to
    place according to a specified criterion.
    """
    __metaclass__ = ABCMeta

    def __init__(self):
        """Initialize parameters of the abstract position handler object."""
        self.order_sizer = {
            TradeTypes.buy_trade: self.buy_size_order,
            TradeTypes.sell_trade: self.sell_size_order,
            TradeTypes.exit_trade: self.exit_size_order
        }

    @abstractmethod
    def buy_size_order(self, symbol, portfolio_handler):
        """This method will be called to determine the number of shares that
        should be bought into when entering a long or short position.
        """
        raise NotImplementedError()

    @abstractmethod
    def sell_size_order(self, symbol, portfolio_handler):
        """This method determines the number of shares to liquidate when selling
        a position.
        """
        raise NotImplementedError()

    def exit_size_order(self, symbol, portfolio_handler):
        """This method liquidates the entire position."""
        try:
            val = portfolio_handler.filled_positions[symbol].quantity
        except KeyError:
            val = 0
        finally:
            return val
