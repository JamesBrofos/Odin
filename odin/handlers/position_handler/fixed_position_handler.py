from .abstract_position_handler import AbstractPositionHandler


class FixedPositionHandler(AbstractPositionHandler):
    """Fixed Position Handler Class

    The fixed position handler object will compute position sizes to be a
    user-specified constant, regardless of equity. This results in all holdings
    consisting of equal numbers of shares, though these positions are likely to
    represent wildly different amounts of equity. This position handler
    corresponds to buying a single lot of shares.
    """
    def __init__(self, default_buy_size, default_sell_size):
        """Initialize parameters of the fixed position handler object."""
        super(FixedPositionHandler, self).__init__()
        self.default_buy_size = default_buy_size
        self.default_sell_size = default_sell_size

    def buy_size_order(self, symbol, portfolio_state):
        """Implementation of abstract base class method."""
        return self.default_buy_size

    def sell_size_order(self, symbol, portfolio_state):
        """Implementation of abstract base class method."""
        return self.default_sell_size
