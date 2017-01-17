from abc import ABCMeta, abstractmethod


class AbstractDataHandler(object):
    """Abstract Data Handler Class

    The data handler is an abstract base class providing an interface for all
    subsequent (inherited) data handlers (both live and historic).

    The goal of a (derived) data handler object is to output a generated set of
    bars for each symbol requested. This will replicate how a live strategy
    would function as current market data would be sent 'down the pipe'. Thus a
    historic and live system will be treated identically by the rest of the
    backtesting suite.
    """
    __metaclass__ = ABCMeta

    def __init__(self, events, symbol_handler, price_handler):
        """Initialize parameters of the abstract data handler object."""
        self.events = events
        self.symbol_handler = symbol_handler
        self.price_handler = price_handler
        self.continue_trading = True

    @abstractmethod
    def update(self):
        """Objects that implement the data handler abstract base class must
        implement a method for obtaining new bars from the data source. This
        method places the most recently available bars onto a data structure for
        access by methods and objects requiring access to the underlying
        financial data.
        """
        raise NotImplementedError()

    @abstractmethod
    def request_prices(self):
        """Request the current price of assets."""
        raise NotImplementedError()

