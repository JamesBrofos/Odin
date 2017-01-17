import queue
import pandas as pd
import datetime as dt
from time import sleep
from ib.opt import ibConnection, message
from ib.ext.TickType import TickType
from .abstract_price_handler import AbstractPriceHandler
from ....utilities.params import IB, PriceFields
from ....utilities.mixins import ContractMixin


class InteractiveBrokersPriceHandler(AbstractPriceHandler, ContractMixin):
    """Interactive Brokers Price Handler Class"""

    def __init__(self):
        """Initialize parameters of the Interactive Brokers price handler
        object.
        """
        super(InteractiveBrokersPriceHandler, self).__init__()
        self.conn = ibConnection(
            clientId=IB.data_handler_id.value, port=IB.port.value
        )
        self.conn.register(self.__tick_price_handler, message.tickPrice)
        if not self.conn.connect():
            raise ValueError(
                "Odin was unable to connect to the Trader Workstation."
            )

        # Set the target field to download data from.
        today = dt.datetime.today()
        open_t, close_t = dt.time(9, 30), dt.time(16)
        cur_t = today.time()
        # If today is a weekday and the timing is correct, then we use the most
        # recently observed price. Otherwise we use the close price.
        if today.weekday() < 5 and cur_t >= open_t and cur_t <= close_t:
            self.field = TickType.LAST
        else:
            self.field = TickType.CLOSE

        # Initialize a pandas panel to store the price data.
        self.bar = pd.Panel(items=[PriceFields.current_price.value])

    def __tick_price_handler(self, msg):
        """Handle incoming prices from the Trader Workstation."""
        if msg.field == self.field:
            # The fourth field corresponds to the most recent observed price.
            # This price is recorded. The nineth field corresponds to the close
            # price.
            tick_id = int(msg.tickerId)
            price = float(msg.price)
            self.bar.ix[0, 0, tick_id] = price

    def request_prices(self, current_date, symbols):
        """Implementation of abstract base class method."""
        # Reset the bar object for the latest assets requested.
        self.bar = pd.Panel(
            items=[PriceFields.current_price.value], major_axis=[current_date],
            minor_axis=symbols
        )
        # Issue requests to Interactive Brokers for the latest price data of
        # each asset in the list of bars.
        for i, s in enumerate(symbols):
            c = self.create_contract(s)
            self.conn.reqMktData(i, c, "", True)

        # Wait a moment.
        sleep(0.5)

        return self.bar
