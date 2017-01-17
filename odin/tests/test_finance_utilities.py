import unittest
import pandas as pd
import datetime as dt
from odin.handlers.data_handler import DatabaseDataHandler
from odin.handlers.symbol_handler import FixedSymbolHandler
from odin.events import EventsQueue
from odin.utilities.finance import modern_portfolio_solve


class FinanceUtilitiesTest(unittest.TestCase):
    def test_modern_portfolio_theory(self):
        q = EventsQueue()
        symbols = ["GOOG", "MS", "AMZN", "GS"]
        sh = FixedSymbolHandler(symbols)
        start, end = dt.datetime(2011, 1, 1), dt.datetime(2017, 1, 1)
        dh = DatabaseDataHandler(q, sh, start, end, 252*5)
        dh.request_prices()
        prices = dh.bars["adj_price_close"]
        # prices = pd.read_csv("/home/james/Desktop/out.csv", index_col=0)
        series = modern_portfolio_solve(prices, 1.)
        # print(series)

if __name__ == "__main__":
    unittest.main()
