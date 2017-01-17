import unittest
import datetime as dt
from odin.handlers.symbol_handler import FixedSymbolHandler
from odin.handlers.data_handler import DatabaseDataHandler
from odin.handlers.data_handler.price_handler import DatabasePriceHandler
from odin.events import EventsQueue
from odin.handlers.portfolio_handler import PortfolioHandler
from odin.utilities.finance import Indices


class PortfolioTest(unittest.TestCase):
    def test_to_datebase_portfolio(self):
        q = EventsQueue()
        start, end = dt.datetime(2015, 1, 2), dt.datetime(2015, 1, 9)
        symbols = [Indices.sp_100_etf, Indices.sp_500_etf]
        sh = FixedSymbolHandler(symbols)
        dh = DatabaseDataHandler(q, sh, start, end, 10)
        max_cap = 1
        capital = 100000.0
        ph = PortfolioHandler(max_cap, dh, "test_portfolio_id", capital)
        ph.to_database_portfolio()

    def test_from_database_portfolio(self):
        pid = "test_portfolio_id"
        q = EventsQueue()
        start, end = dt.datetime(2015, 1, 2), dt.datetime(2015, 1, 9)
        symbols = [Indices.sp_100_etf, Indices.sp_500_etf]
        sh = FixedSymbolHandler(symbols)
        dh = DatabaseDataHandler(q, sh, start, end, 10)
        ph = PortfolioHandler.from_database_portfolio(pid, dh)
        self.assertEqual(ph.capital, 100000.0)
        self.assertEqual(ph.maximum_capacity, 1)
        self.assertEqual(ph.portfolio_id, pid)
        self.assertTrue("SPY" in ph.filled_positions)


if __name__ == "__main__":
    unittest.main()
