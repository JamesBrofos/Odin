from .fund_event import FundEvent
from ...utilities.params import Events


class RebalanceEvent(FundEvent):
    """Rebalance Fund Event Class

    Odin will periodically ensure that the capital investment in long and short
    portfolios of a fund remains consistent with some predetermined weighting.
    For many cases, this will be full dollar-neutrality, corresponding to an
    equal split of equity. This event triggers rebalancing.
    """
    def __init__(self, datetime):
        """Initialize parameters of the rebalance event object."""
        super(RebalanceEvent, self).__init__(Events.rebalance, datetime)

