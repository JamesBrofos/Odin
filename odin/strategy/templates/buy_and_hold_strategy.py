import pandas as pd
from ..abstract_strategy import AbstractStrategy
from ...utilities.mixins.strategy_mixins import (
    LongStrategyMixin,
    EqualBuyProportionMixin
)


class BuyAndHoldStrategy(LongStrategyMixin, EqualBuyProportionMixin):
    """Buy And Hold Strategy Class

    The buy and hold strategy is a passive approach to investing where a
    position is entered and then never exited. Nor are additional positions
    taken up. This is a strategy that is both very scalable and suitable for
    backtesting core functionalities.
    """
    def buy_indicator(self, feats):
        """Implementation of abstract base class method."""
        return True

    def sell_indicator(self, feats):
        """Implementation of abstract base class method."""
        return False

    def exit_indicator(self, feats):
        """Implementation of abstract base class method."""
        return False

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
