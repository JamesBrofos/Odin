from .portfolio_event import PortfolioEvent
from ...utilities.params import Events


class SignalEvent(PortfolioEvent):
    """Signal Event Class

    Handles the event of sending a Signal from a Strategy object. This is
    received by a Portfolio object and acted upon.
    """
    def __init__(self, symbol, trade_type, direction, datetime, portfolio_id):
        """Initialize parameters of the signal event object."""
        super(SignalEvent, self).__init__(
            symbol, trade_type, direction, Events.signal, datetime, portfolio_id
        )

    def __str__(self):
        """String representation of the signal event object."""
        return "{}\t{}\t{}\t{}\t{}".format(
            self.event_type, self.datetime.strftime("%Y-%m-%d %H:%M:%S"),
            self.symbol, self.direction, self.trade_type
        )
