from ...params import Directions
from ....strategy import AbstractStrategy


class LongStrategyMixin(AbstractStrategy):
    """Long Strategy Mixin Class

    This class should be inherited by strategies that are long-only.
    """
    def compute_direction(self, feats):
        """Implementation of abstract base class method."""
        return Directions.long_dir


class ShortStrategyMixin(AbstractStrategy):
    """Short Strategy Mixin Class

    This class should be inherited by strategies that are short-only.
    """
    def compute_direction(self, feats):
        """Implementation of abstract base class method."""
        return Directions.short_dir
