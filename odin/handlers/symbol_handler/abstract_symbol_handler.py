from abc import ABCMeta, abstractmethod


class AbstractSymbolHandler(object):
    """Abstract Symbol Handler Class

    The symbol handler class is responsible for determining which stocks should
    have their prices retrieved for processing and potential trading during the
    next trading period.
    """
    __metaclass__ = ABCMeta

    def __init__(self, portfolio_handlers):
        """Initialize parameters of the abstract symbol handler object."""
        self.portfolio_handlers = portfolio_handlers

    @abstractmethod
    def select_symbols(self, date):
        """Select symbols to be processed during the next trading period. This
        function takes as input the price data from the current trading period,
        which can be used to generate rankings of stocks subsequently.
        """
        raise NotImplementedError()

    def append_positions(self, selected):
        """"""
        set_selected = set(selected)
        for p in self.portfolio_handlers:
            for pos in p.filled_positions:
                set_selected.add(pos)

        return list(set_selected)
