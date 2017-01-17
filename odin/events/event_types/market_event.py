from .event import Event
from ...utilities.params import Events

class MarketEvent(Event):
    """Market Event Class

    Handles the event of receiving a new market update with corresponding bars.

    Parameters
    ----------
    datetime: Refer to base class documentation.
    """
    def __init__(self, datetime):
        """Initialize parameters of the market event object."""
        super(MarketEvent, self).__init__(Events.market, datetime)
