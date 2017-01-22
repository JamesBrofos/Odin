import datetime as dt
from time import sleep
from ib.opt import ibConnection, Connection, message
from ib.ext.Contract import Contract
from ib.ext.Order import Order
from .abstract_execution_handler import AbstractExecutionHandler
from ...utilities.params import action_dict, IB, ib_commission, ib_silent_errors
from ...utilities.mixins import ContractMixin
from ...events import FillEvent


class InteractiveBrokersExecutionHandler(
        AbstractExecutionHandler, ContractMixin
):
    """Interactive Brokers Execution Handler

    The Interactive Brokers execution handler constructs pairs of contracts and
    orders to be sent to the brokerage. This execution handler is used in live
    trading to actually fill orders that are requested; it can, however, be used
    in either real or paper trading environments. The TraderWorkstation needs to
    be online before this module can function.
    """
    def __init__(self, events):
        """Initialize parameters for the interactive brokers execution handler
        object.
        """
        super(InteractiveBrokersExecutionHandler, self).__init__(events, True)
        self.conn = Connection.create(
            clientId=IB.execution_handler_id.value, port=IB.port.value
        )
        self.conn.register(self.__error_handler, message.error)
        self.conn.registerAll(self.__reply_handler)
        if not self.conn.connect():
            raise ValueError(
                "Odin was unable to connect to the Trader Workstation."
            )
        self.orders = {}
        self.order_id = 1
        # It is important to sleep momentarily so that we can sync with the
        # latest order identifier from Interactive Brokers.
        sleep(1)

    def __error_handler(self, msg):
        """Process errors from the Interactive Brokers Trader Workstation by
        displaying them on standard out.
        """
        if msg.errorCode not in ib_silent_errors:
            print("Interactive Brokers execution handler error: {}".format(msg))

    def __reply_handler(self, msg):
        """This function handles responses from the TraderWorkstation server. It
        has two primary duties. The first of these is to determine the next
        valid trade identifier so that we know what identifier to assign to our
        orders when they are submitted to the brokerage. The second is to detect
        when an order has been filled as to place that fill event into the queue
        for processing by the portfolio.
        """
        if msg.typeName == "nextValidId":
            self.order_id = int(msg.orderId)
        elif msg.typeName == "orderStatus" and msg.status == "Filled":
            o = self.orders[msg.orderId]
            if not o["filled"]:
                # Extract variables upon order fill.
                order_id = msg.orderId
                symbol = o["symbol"]
                quantity = msg.filled
                trade_type = o["trade_type"]
                direction = o["direction"]
                fill_cost = msg.avgFillPrice * quantity
                commission = ib_commission(quantity, msg.avgFillPrice)
                datetime = dt.datetime.today()
                pid = o["portfolio_id"]
                is_live = self.is_live
                # Place the fill event into the queue and mark the order as
                # completed.
                fill_event = FillEvent(
                    symbol, quantity, trade_type, direction, fill_cost,
                    commission, datetime, pid, is_live
                )
                o["filled"] = True
                self.events.put(fill_event)

    def create_order(self, action, quantity):
        """Create an Interactive Brokers order object. This specifies whether or
        not we are selling or buying the asset, the quantity to exchange, and
        the order type of the trade (which is assumed to be a market order).
        """
        o = Order()
        o.m_orderType = "MKT"
        o.m_totalQuantity = quantity
        o.m_action = action
        return o

    def execute_order(self, order_event):
        """Implementation of abstract base class method."""
        symbol = order_event.symbol
        quantity = order_event.quantity
        direction = order_event.direction
        trade_type = order_event.trade_type
        action = action_dict[(direction, trade_type)].value

        # Create orders and contracts for the trade to be submitted to the
        # brokerage.
        c = self.create_contract(symbol)
        o = self.create_order(action, quantity)
        self.orders[self.order_id] = {
            "filled": False,
            "symbol": symbol,
            "trade_type": order_event.trade_type,
            "direction": order_event.direction,
            "portfolio_id": order_event.portfolio_id,
        }
        self.conn.placeOrder(self.order_id, c, o)
        sleep(2)
        # Increment the order identifier for future trades.
        self.order_id += 1
