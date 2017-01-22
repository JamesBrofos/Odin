import unittest
import datetime as dt
from odin.events import EventsQueue
from odin.utilities.finance import Indices
from odin.handlers.data_handler import DatabaseDataHandler
from odin.handlers.data_handler.price_handler import DatabasePriceHandler
from odin.handlers.symbol_handler import (
    FixedSymbolHandler, DollarVolumeSymbolHandler
)


class SymbolHandlerTest(unittest.TestCase):
    def test_fixed_symbol_handler(self):
        q = EventsQueue()
        start, end = dt.datetime(2015, 1, 2), dt.datetime(2015, 1, 9)
        symbols = [Indices.sp_100_etf.value, Indices.sp_500_etf.value]
        sh = FixedSymbolHandler(symbols, [])
        dh = DatabaseDataHandler(q, sh, start, end, 10)
        self.assertEqual(set(sh.select_symbols(dh.current_date)), set(symbols))

    def test_dollar_volume_symbol_handler(self):
        q = EventsQueue()
        start, end = dt.datetime(2015, 1, 2), dt.datetime(2015, 1, 9)
        symbols = [Indices.sp_100_etf, Indices.sp_500_etf]
        sh = DollarVolumeSymbolHandler(1, [], None)
        dh = DatabaseDataHandler(q, sh, start, end, 10)
        sel = set([s for s in sh.select_symbols(dh.current_date)])
        self.assertEqual(
            sel, set((Indices.sp_500_etf.value, ))
        )


if __name__ == "__main__":
    unittest.main()
