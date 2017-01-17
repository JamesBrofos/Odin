from .portfolio_event import PortfolioEvent
from ...utilities.params import Events, IOFiles


class FillEvent(PortfolioEvent):
    """Fill Event Class

    Encapsulates the notion of a filled order, as returned from a brokerage.
    Stores the quantity of an instrument actually filled and at what price. In
    addition, stores the commission of the trade from the brokerage.
    """
    def __init__(
            self, symbol, quantity, trade_type, direction, fill_cost,
            commission, datetime, portfolio_id, is_live
    ):
        """Initialize parameters of the fill event object."""
        super(FillEvent, self).__init__(
            symbol, trade_type, direction, Events.fill, datetime,
            portfolio_id
        )
        self.quantity = quantity
        self.fill_cost = fill_cost
        self.commission = commission
        self.price = self.fill_cost / self.quantity
        self.is_live = is_live

    def __str__(self):
        """String representation of the fill event object."""
        return "{}\t{}\t{}\t{}\t{}\t{}\t{:0.2f}".format(
            self.event_type, self.datetime.strftime(IOFiles.date_format.value),
            self.symbol, self.direction, self.trade_type, self.quantity,
            self.fill_cost
        )
