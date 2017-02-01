from ....strategy import AbstractStrategy


class EqualBuyProportionMixin(AbstractStrategy):
    """Equal Proportion Mixin Class

    This class should be inherited by strategies that intend to partition their
    equity equally among the assets that are purchased.
    """
    def compute_buy_proportion(self, feats):
        """Implementation of abstract base class method."""
        return 1.0 / self.portfolio.portfolio_handler.maximum_capacity


class TotalSellProportionMixin(AbstractStrategy):
    """Total Sell Proportion Mixin Class

    This class will instruct the strategy to entirely liquidate a position when
    a sell signal is created. Note that, in general, a sell signal is distinct
    from an exit signal, though choosing the sell a position entirely makes the
    two equivalent.
    """
    def compute_sell_proportion(self, feats):
        """Implementation of abstract base class method."""
        return 1.0
