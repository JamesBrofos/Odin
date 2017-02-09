from ....strategy import AbstractStrategy


class AlwaysBuyIndicatorMixin(AbstractStrategy):
    """Always Buy Strategy Mixin"""
    def buy_indicator(self, feats):
        """Implementation of abstract base class method."""
        return True


class NeverSellIndicatorMixin(AbstractStrategy):
    """Never Sell Strategy Mixin"""
    def sell_indicator(self, feats):
        """Implementation of abstract base class method."""
        return False


class NeverExitIndicatorMixin(AbstractStrategy):
    """Never Exit Strategy Mixin"""
    def exit_indicator(self, feats):
        """Implementation of abstract base class method."""
        return False
