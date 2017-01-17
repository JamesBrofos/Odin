from .portfolio_event import PortfolioEvent
from ...utilities.params import Events, IOFiles


class OrderEvent(PortfolioEvent):
    """Order Event Class

    Handles the event of sending an Order to an execution system. The order
    contains a symbol (e.g. 'GOOG'), a type ('BUY', 'SELL', or 'EXIT'),
    quantity, and a direction (long or short).
    """
    def __init__(
            self, symbol, quantity, trade_type, direction, datetime,
            portfolio_id
    ):
        """Initialize parameters of the order event object."""
        super(OrderEvent, self).__init__(
            symbol, trade_type, direction, Events.order, datetime,
            portfolio_id
        )
        self.quantity = quantity

    def __str__(self):
        """String representation of the order event object."""
        return "{}\t{}\t{}\t{}\t{}\t{}".format(
            self.event_type, self.datetime.strftime(IOFiles.date_format.value),
            self.symbol, self.direction, self.trade_type, self.quantity
        )
