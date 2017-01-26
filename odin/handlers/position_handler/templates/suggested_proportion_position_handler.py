from ..abstract_position_handler import AbstractPositionHandler


class SuggestedProportionPositionHandler(AbstractPositionHandler):
    """Suggested Proportion Position Handler Class

    This class will (naively) utilize the suggested proportion of equity
    provided by the signal event object to allocate the portfolio's equity.
    """
    def compute_buy_weights(self, signal_event, portfolio_handler):
        """Implementation of abstract base class method."""
        return {signal_event.symbol: signal_event.suggested_proportion}

    def compute_sell_weights(self, signal_event, portfolio_handler):
        """Implementation of abstract base class method."""
        return {signal_event.symbol: signal_event.suggested_proportion}
