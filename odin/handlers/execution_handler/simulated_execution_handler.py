from .abstract_execution_handler import AbstractExecutionHandler
from ...events import FillEvent
from ...utilities import params


class SimulatedExecutionHandler(AbstractExecutionHandler):
    """Simulated Execution Handler Class

    The simulated execution handler simply converts all order objects into their
    equivalent fill objects automatically without latency, slippage or
    fill-ratio issues.

    This allows a straightforward 'first go' test of any strategy, before
    implementation with a more sophisticated execution handler. The simulated
    execution handler incorporates both commission fees as well as transaction
    costs incurred by simply interacting with (buying or selling) an asset. The
    assumed commission for a one-directional trade with IB is $1.00.
    """
    def __init__(self, data_handler, transaction_cost=0.0005):
        """Initialize parameters of the simulated execution handler object."""
        super(SimulatedExecutionHandler, self).__init__(
            data_handler.events, False
        )
        self.data_handler = data_handler
        self.transaction_cost = transaction_cost

    def execute_order(self, order_event):
        """Implementation of abstract base class method."""
        # Construct quantities for the simulated fill event.
        symbol = order_event.symbol
        quantity = order_event.quantity
        trade_type = order_event.trade_type
        direction = order_event.direction
        action = params.action_dict[(direction, trade_type)]
        datetime = order_event.datetime
        pid = order_event.portfolio_id

        # Assume the fill price to be the average of the day's high and low and
        # incorporate transaction costs. If the action is to sell the asset,
        # then price moves down, otherwise for buying actions, the price is
        # driven upward.
        price_id = [
            params.PriceFields.sim_low_price.value,
            params.PriceFields.sim_high_price.value
        ]
        fill_price = self.data_handler.prices.ix[price_id, 0, symbol].mean()
        fill_cost = fill_price * quantity
        # Change cost according to whether or not shares are bought or sold.
        # This is distinct from trade type.
        if action == params.Actions.sell:
            fill_cost *= (1. - self.transaction_cost)
        elif action == params.Actions.buy:
            fill_cost *= (1. + self.transaction_cost)

        # Place the fill event in the queue.
        commission = params.ib_commission(quantity, fill_price)
        fill_event = FillEvent(
            symbol, quantity, trade_type, direction, fill_cost, commission,
            datetime, pid, self.is_live
        )
        self.events.put(fill_event)
