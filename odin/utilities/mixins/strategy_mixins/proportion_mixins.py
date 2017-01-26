from ....strategy import AbstractStrategy


class EqualProportionMixin(AbstractStrategy):
    """Equal Proportion Mixin Class

    This class should be inherited by strategies that intend to partition their
    equity equally among the assets that are purchased.
    """
    def compute_proportion(self, feats):
        """Implementation of abstract base class method."""
        if feats.name not in self.portfolio.portfolio_handler.filled_positions:
            return 1.0 / self.portfolio.portfolio_handler.maximum_capacity
        else:
            return 1.0
