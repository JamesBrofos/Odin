from .event import Event


class PortfolioEvent(Event):
    """Portfolio Event Class

    This class is to capture all universal properties of events impacting an
    individual portfolio.

    Parameters
    ----------
    event_type, datetime: Refer to base class documentation.
    symbol: String.
        The ticker symbol about which the event is taking place.
    trade_type: String.
        Whether or not the security is being bought, sold, or completely exited.
    direction: String.
        A string indicator of whether we are long or short the security.
    portfolio_id: String.
        A unique identifier assigned to the portfolio.
    """
    def __init__(
            self, symbol, trade_type, direction, event_type, datetime,
            portfolio_id
    ):
        """Initialize parameters of the portfolio event object."""
        super(PortfolioEvent, self).__init__(event_type, datetime)
        self.symbol = symbol
        self.trade_type = trade_type
        self.direction = direction
        self.portfolio_id = portfolio_id

