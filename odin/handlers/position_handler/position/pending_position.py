from ....utilities.params import action_dict


class PendingPosition(object):
    """Pending Position Class

    The pending position object represents a position that has been sent to the
    brokerage to be filled (and become a filled position), but which has not yet
    been completed. The pending position represents simply the ticker, the
    quantity of shares in the position, whether or not the strategy is long or
    short the stock, and an identifier for the portfolio.
    """
    def __init__(
            self, symbol, quantity, direction, trade_type, portfolio_id
    ):
        """Initialize parameters of the pending position object."""
        self.symbol = symbol
        self.quantity = quantity
        self.direction = direction
        self.portfolio_id = portfolio_id
        self.trade_type = trade_type
        self.action = action_dict[(self.direction, self.trade_type)]
