class EquityMixin(object):
    """Equity Mixin Class"""

    @property
    def equity(self):
        """Computes the total equity of the portfolio. This is simply the sum of
        the free capital available to the portfolio and the current market value
        of each position in the portfolio.
        """
        pos = self.filled_positions.values()
        return self.capital + sum([p.relative_value for p in pos])
