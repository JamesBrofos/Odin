import pandas as pd
from odin.strategy import AbstractStrategy


class BuySellStrategy(AbstractStrategy):
    """Buy Sell Strategy Class

    The buy sell strategy is a stupid strategy that just buys and sells assets
    at every opportunity. This is just for testing functionality and isn't good
    for much else.
    """
    def buy_indicator(self, feats):
        """Implementation of abstract base class method."""
        return True

    def sell_indicator(self, feats):
        """Implementation of abstract base class method."""
        return False

    def exit_indicator(self, feats):
        """Implementation of abstract base class method."""
        return True

    def generate_features(self):
        """Implementation of abstract base class method."""
        symbols = self.portfolio.data_handler.bars.ix[
            "adj_price_open", -1, :
        ].dropna().index
        return pd.DataFrame(index=symbols)

    def generate_priority(self, feats):
        """Implementation of abstract base class method."""
        return self.portfolio.data_handler.bars.ix[
            "adj_price_open", -1, :
        ].dropna().index
