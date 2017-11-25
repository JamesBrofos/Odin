import datetime as dt
import numpy as np
from odin_securities.queries import gets
from .abstract_database_data_handler import AbstractDatabaseDataHandler
from ..price_handler import DatabasePriceHandler
from ....events import MarketEvent


class DatabaseDataHandler(AbstractDatabaseDataHandler):
    """Database Data Handler Class

    This class interfaces with the Odin Securities Postgres database to obtain
    the price and volume data for the requested symbols.
    """
    def __init__(
            self, events, symbol_handler, start_date, end_date, n_init
    ):
        """Initialize parameters of the database data handler object."""
        price_handler = DatabasePriceHandler()
        # Determine which are valid trading days and set the start and end
        # period of the backtest.
        self.sessions = gets.standard_sessions(
            start_date, end_date
        )["datetime"]
        self.start_date = self.sessions.iloc[0]
        self.end_date = self.sessions.iloc[-1]
        self.yield_dates = self.__yield_dates()
        # Call the super method to initialize the remaining parameters.
        super(DatabaseDataHandler, self).__init__(
            events, symbol_handler, price_handler, n_init, self.start_date
        )

    def __yield_dates(self):
        """Create an iterator over the dates contained in the historical
        download.
        """
        for date in self.sessions:
            yield date

    def request_prices(self):
        """Implementation of abstract base class method."""
        try:
            # TODO: Check if it is possible to reuse the old selected variable
            #       from the update method.
            selected = self.symbol_handler.select_symbols(self.current_date)
            self.current_date = next(self.yield_dates)
            self.prices = self.price_handler.request_prices(
                self.current_date, selected
            )
        except StopIteration:
            self.continue_trading = False
        else:
            self.events.put(MarketEvent(self.current_date))
