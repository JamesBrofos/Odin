from .portfolio_event import PortfolioEvent
from ...utilities.params import Events


class SignalEvent(PortfolioEvent):
    """Signal Event Class

    Handles the event of sending a Signal from a Strategy object. This is
    received by a Portfolio object and acted upon.
    """
    def __init__(
            self,
            symbol,
            suggested_proportion,
            trade_type, direction,
            datetime,
            portfolio_id
    ):
        """Initialize parameters of the signal event object."""
        super(SignalEvent, self).__init__(
            symbol, trade_type, direction, Events.signal,
            datetime, portfolio_id
        )
        # N.B.: When the trade type of the signal indicates a buy, the suggested
        # proportion is the fraction of the portfolio's equity which will be
        # allocated to this position. On the other hand, when the trade type is
        # a sell, the proportion corresponds to the fraction of the existing
        # number of shares that should be liquidated.
        self.suggested_proportion = suggested_proportion

    def __str__(self):
        """String representation of the signal event object."""
        return "{}\t{}\t{}\t{}\t{}".format(
            self.event_type,
            self.datetime.strftime("%Y-%m-%d %H:%M:%S"),
            self.symbol,
            self.direction,
            self.trade_type
        )
