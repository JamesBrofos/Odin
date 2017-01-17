from ...utilities.params import IOFiles


class Event(object):
    """Event Class

    Odin processes trading information by handling events of different kinds. All
    of the events used by Odin are defined in this file. Excluding market events,
    there are two kinds of events: The first of these are events at the portfolio
    level, which handle generating trading signals, submitting order events, and
    processing fill events from the brokerage. The other kind of event pertains
    to the level of the fund: This events determine when the fund rebalances its
    long and short positions as well as when management fees are subtracted from
    the equity holdings of the fund.

    At the most abstract level, an event is described by its type and the date
    and time at which the event occurred.

    Parameters
    ----------
    event_type: String.
        A string indicator of the type of event that is being represented.
    datetime: Datetime object.
        The date and time at which the event was created.
    """
    def __init__(self, event_type, datetime):
        """Initialize parameters of the event object."""
        self.datetime = datetime
        self.event_type = event_type

    def __str__(self):
        """String representation of the market event object."""
        return "{}\t{}".format(
            self.event_type, self.datetime.strftime(IOFiles.date_format.value)
        )
