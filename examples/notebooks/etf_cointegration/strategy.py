import numpy as np
import pandas as pd
from odin.strategy import AbstractStrategy
from odin.strategy.templates import BuyAndHoldStrategy
from odin.utilities.params import Directions
from odin.utilities.mixins.strategy_mixins import (
    EqualBuyProportionMixin, TotalSellProportionMixin
)


class CointegratedETFStrategy(
    EqualBuyProportionMixin, TotalSellProportionMixin
):  
    def compute_direction(self, feats):
        """Implementation of abstract base class method."""
        if feats.name == "ARNC":
            if feats["z-score"] < -1.5:
                return Directions.long_dir
            elif feats["z-score"] > 1.5:
                return Directions.short_dir
        elif feats.name == "UNG":
            if feats["z-score"] < -1.5:
                return Directions.short_dir
            elif feats["z-score"] > 1.5:
                return Directions.long_dir

    def buy_indicator(self, feats):
        """Implementation of abstract base class method."""
        return (
            feats["z-score"] < -1.5 or
            feats["z-score"] > 1.5
        )

    def sell_indicator(self, feats):
        """Implementation of abstract base class method."""
        return False

    def exit_indicator(self, feats):
        """Implementation of abstract base class method."""
        pos = self.portfolio.portfolio_handler.filled_positions["ARNC"]
        d = pos.direction
        return (
            (feats["z-score"] > -0.5 and d == Directions.long_dir) or
            (feats["z-score"] < 0.5 and d == Directions.short_dir)
        )

    def generate_features(self):
        """Implementation of abstract base class method."""
        bars = self.portfolio.data_handler.bars.ix[:, -15:, :]
        prices = bars["adj_price_close"]
        weights = np.array([1.0, -1.213])
        feats = pd.DataFrame(index=bars.minor_axis)
        ts = prices.dot(weights)
        feats["z-score"] = (ts.ix[-1] - ts.mean()) / ts.std()
        return feats

    def generate_priority(self, feats):
        """Implementation of abstract base class method."""
        return self.portfolio.data_handler.bars.ix[
            "adj_price_open", -1, :
        ].dropna().index
