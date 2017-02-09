from ....strategy import AbstractStrategy


class DefaultPriorityMixin(AbstractStrategy):
    """Default Priority Mixin Class

    This class simply retrieves the symbols that are available at the conclusion
    of the previous day and returns them in the same order that they are in the
    bars panel object.
    """
    def generate_priority(self, feats):
        """Implementation of abstract base class method."""
        return self.portfolio.data_handler.bars.ix[
            "adj_price_close", -1, :
        ].dropna().index
