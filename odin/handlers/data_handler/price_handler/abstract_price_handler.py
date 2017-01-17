from abc import ABCMeta, abstractmethod


class AbstractPriceHandler(object):
    """Abstract Price Handler Class

    Price handler objects are responsible for retrieving either live or
    simulated price data for particular assets. This information is then used
    to make entry or exit decisions for positions, and to size out the quantity
    of shares to transact.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def request_prices(self, current_date, symbols):
        """Request prices for assets on the current date."""
        raise NotImplementedError()



