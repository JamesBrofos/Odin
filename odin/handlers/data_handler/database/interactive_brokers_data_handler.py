import datetime as dt
import numpy as np
from ....events import MarketEvent
from .abstract_database_data_handler import AbstractDatabaseDataHandler
from ..price_handler import InteractiveBrokersPriceHandler


class InteractiveBrokersDataHandler(AbstractDatabaseDataHandler):
    """Interactive Brokers Data Handler Class
    """
    def __init__(self, events, symbol_handler, n_init):
        """Initialize parameters of the Interactive Brokers data handler object.
        """
        price_handler = InteractiveBrokersPriceHandler()
        super(InteractiveBrokersDataHandler, self).__init__(
            events, symbol_handler, price_handler, n_init, dt.datetime.today()
        )

    def request_prices(self):
        """Implementation of abstract base class method."""
        selected = self.symbol_handler.select_symbols(self.current_date)
        self.current_date = dt.datetime.today()
        self.prices = self.price_handler.request_prices(
            self.current_date, selected
        )
        self.events.put(MarketEvent(self.current_date))
