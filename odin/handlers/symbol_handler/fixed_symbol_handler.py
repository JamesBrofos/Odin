from .abstract_symbol_handler import AbstractSymbolHandler


class FixedSymbolHandler(AbstractSymbolHandler):
    """Fixed Symbol Handler Class

    The fixed symbol handler allows the user to easily specify a fixed set of
    tickers for which to query data. This is the simplest variety of symbol
    handler since it is invariant to the date parameter provided to the symbol
    selection method.

    Parameters
    ----------
    symbols (optional): List of strings.
        An input specifying a particular list of tickers to which the dollar
        volume ordering should be restricted.
    """
    def __init__(self, symbols):
        """Initialize parameters of the fixed symbol handler object."""
        self.symbols = symbols

    def select_symbols(self, date):
        """Implementation of abstract base class method."""
        return self.symbols

