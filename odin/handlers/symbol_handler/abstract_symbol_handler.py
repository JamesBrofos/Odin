from abc import ABCMeta, abstractmethod


class AbstractSymbolHandler(object):
    """Abstract Symbol Handler Class

    The symbol handler class is responsible for determining which stocks should
    have their prices retrieved for processing and potential trading during the
    next trading period.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def select_symbols(self, date):
        """Select symbols to be processed during the next trading period. This
        function takes as input the price data from the current trading period,
        which can be used to generate rankings of stocks subsequently.
        """
        raise NotImplementedError()
