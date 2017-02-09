import pandas as pd
from ..abstract_strategy import AbstractStrategy
from ...utilities.mixins.strategy_mixins import (
    LongStrategyMixin,
    EqualBuyProportionMixin,
    DefaultPriorityMixin,
    DefaultFeaturesMixin,
    AlwaysBuyIndicatorMixin,
    NeverSellIndicatorMixin,
    NeverExitIndicatorMixin,
)


class BuyAndHoldStrategy(
        LongStrategyMixin,
        EqualBuyProportionMixin,
        DefaultPriorityMixin,
        DefaultFeaturesMixin,
        AlwaysBuyIndicatorMixin,
        NeverSellIndicatorMixin,
        NeverExitIndicatorMixin,
):
    """Buy And Hold Strategy Class

    The buy and hold strategy is a passive approach to investing where a
    position is entered and then never exited. Nor are additional positions
    taken up. This is a strategy that is both very scalable and suitable for
    backtesting core functionalities.
    """
