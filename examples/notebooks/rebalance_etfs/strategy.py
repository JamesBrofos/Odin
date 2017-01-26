import pandas as pd
from odin.strategy import AbstractStrategy
from odin.strategy.templates import BuyAndHoldStrategy
from odin.utilities.mixins.strategy_mixins import LongStrategyMixin


class BuyAndHoldSpyderStrategy(BuyAndHoldStrategy):
    def buy_indicator(self, feats):
        return feats.name in ("SPY", )


class RebalanceETFStrategy(LongStrategyMixin):
    def compute_proportion(self, feats):
        """Implementation of abstract base class method."""
        if feats.name not in self.portfolio.portfolio_handler.filled_positions:
            if feats.name == "SPY":
                return 0.6
            elif feats.name == "AGG":
                return 0.4
        else:
            return 1.0

    
    def buy_indicator(self, feats):
        """Implementation of abstract base class method."""
        return True

    def sell_indicator(self, feats):
        """Implementation of abstract base class method."""
        return False

    def exit_indicator(self, feats):
        """Implementation of abstract base class method."""
        symbol = feats.name
        pos = self.portfolio.portfolio_handler.filled_positions[symbol]
        date = self.portfolio.data_handler.current_date
        return pos.compute_holding_period(date).days > 63

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
