from odin_securities.queries import gets
from .abstract_symbol_handler import AbstractSymbolHandler
from ...utilities.finance import Indices, untradeable_assets


class DollarVolumeSymbolHandler(AbstractSymbolHandler):
    """Dollar Volume Symbol Handler Class

    The dollar volume symbol handler selects assets by ranking stocks according
    to the total dollar volume transacted during the previous trading session.
    The symbol handler ignores the S&P 100 and S&P 500 indices which have huge
    volume.
    """
    def __init__(self, n, symbols=None):
        """Initialize parameters of the dollar volume symbol handler object.

        Parameters
        ----------
        n: Integer.
            The number of assets to take from the ranking according to dollar
            volume; i.e. the top stocks according to dollar volume during the
            previous trading session.
        symbols (optional): List of strings.
            An input specifying a particular list of tickers to which the dollar
            volume ordering should be restricted.
        """
        self.n = n
        self.symbols = symbols

    def select_symbols(self, date):
        """Implementation of abstract base class method."""
        bars = gets.prices(date, symbols=self.symbols)
        dv = bars.ix["adj_price_close", -1, :] * bars.ix["adj_volume", -1, :]
        rank = dv.sort_values(ascending=False).dropna()
        return rank.index.drop(untradeable_assets, errors="ignore")[:self.n]
