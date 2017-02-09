import pandas as pd
from odin.strategy.indicators import MovingAverage as MA
from odin.utilities.mixins.strategy_mixins import (
    LongStrategyMixin,
    EqualBuyProportionMixin, 
    TotalSellProportionMixin,
    DefaultPriorityMixin,
    NeverSellIndicatorMixin
)


class MovingAverageCrossoverStrategy(
    LongStrategyMixin, 
    EqualBuyProportionMixin, 
    TotalSellProportionMixin,
    DefaultPriorityMixin,
    NeverSellIndicatorMixin
):
    def buy_indicator(self, feats):
        """Implementation of abstract base class method."""
        return (
            feats.name == "AAPL" and
            feats["short_mavg"] > feats["long_mavg"]
        )

    def exit_indicator(self, feats):
        """Implementation of abstract base class method."""
        return (
            feats["long_mavg"] > feats["short_mavg"]
        )

    def generate_features(self):
        """Implementation of abstract base class method."""
        series = self.portfolio.data_handler.bars["adj_price_close"]
        feats = pd.DataFrame(index=series.columns)
        feats["long_mavg"] = MA(200).simple_moving_average(series)
        feats["short_mavg"] = MA(50).simple_moving_average(series)
        return feats