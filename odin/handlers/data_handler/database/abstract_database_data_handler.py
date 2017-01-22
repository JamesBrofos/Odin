import datetime as dt
import numpy as np
from abc import ABCMeta
from odin_securities.queries import gets
from ....events import MarketEvent
from ..abstract_data_handler import AbstractDataHandler


class AbstractDatabaseDataHandler(AbstractDataHandler):
    """Abstract Database Data Handler Class

    This abstract class integrates the data handler objects with Odin's
    securities database, allowing them to query price data. In particular it
    supports obtaining the initial set of bars and then subsequently updating
    those bars for assets specified by the symbol handler.
    """
    __metaclass__ = ABCMeta

    def __init__(
            self, events, symbol_handler, price_handler, n_init, current_date
    ):
        """Initialize parameters of the abstract database data handler object.
        """
        super(AbstractDatabaseDataHandler, self).__init__(
            events, symbol_handler, price_handler
        )
        self.n_init = n_init
        self.current_date = current_date
        # Download initial bar data for the database data handler. This is
        # necessary to allow trading on the first day of sessions; otherwise,
        # we would not have data in time.
        self.__query_initial_bars()

    def __query_initial_bars(self):
        """Download an appropriate amount of initial data to allow the trading
        algorithm to begin at the beginning of the historical time-frame. This
        avoids needlessly having to wait for the algorithm to obtain a 'critical
        mass' of data before executing trades.
        """
        end_date = self.current_date - dt.timedelta(days=1)
        start_date = end_date - dt.timedelta(days=self.n_init)
        self.bars = gets.prices(start_date, end_date)
        selected = self.symbol_handler.select_symbols(self.bars.major_axis[-1])
        self.bars.drop(
            [s for s in self.bars.minor_axis if s not in selected],
            axis=2, inplace=True
        )

    def update(self):
        """Implementation of abstract base class method."""
        # N.B.: When update is called after all of the time period's events have
        #       been processed, the bars are changed!
        selected = self.symbol_handler.select_symbols(self.current_date)
        self.bars = gets.prices(
            self.current_date - dt.timedelta(days=self.n_init),
            self.current_date, selected
        )

