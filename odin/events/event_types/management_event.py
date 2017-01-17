from .fund_event import FundEvent
from ...utilities.params import Events


class ManagementEvent(FundEvent):
    """Fund Management Event Class

    Portfolio managers take a fee from the fund at the conclusion of the year.
    Typically, this is some percentage of the assets-under-management (AUM) and
    another percentage of the returns.
    """
    def __init__(self, datetime):
        """Initialize parameters of the management event object."""
        super(ManagementEvent, self).__init__(Events.management, datetime)

