import unittest
import pandas as pd
import datetime as dt
from odin.handlers.data_handler import DatabaseDataHandler
from odin.handlers.symbol_handler import FixedSymbolHandler
from odin.events import EventsQueue
from odin.utilities.finance.modern_portfolio_theory import (
    solve_markowitz, solve_black_litterman
)


class FinanceUtilitiesTest(unittest.TestCase):
    def test_markowitz(self):
        q = EventsQueue()
        symbols = ["GOOG", "MS", "AMZN", "GS"]
        sh = FixedSymbolHandler(symbols, [])
        start, end = dt.datetime(2011, 1, 1), dt.datetime(2017, 1, 1)
        dh = DatabaseDataHandler(q, sh, start, end, 252*5)
        dh.request_prices()
        prices = dh.bars["adj_price_close"]
        series = solve_markowitz(prices, 1.)


if __name__ == "__main__":
    unittest.main()
