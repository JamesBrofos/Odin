import datetime as dt
import unittest
from odin.utilities.finance import Indices
from odin.handlers.data_handler.price_handler import (
    DatabasePriceHandler, InteractiveBrokersPriceHandler
)


class PriceHandlerTest(unittest.TestCase):
    def test_database_price_handler(self):
        date = dt.datetime(2016, 12, 21)
        ph = DatabasePriceHandler()
        symbols = [Indices.sp_100_etf.value, Indices.sp_500_etf.value]
        prices = ph.request_prices(date, symbols)
        self.assertEqual(set(prices.minor_axis), set(symbols))
        self.assertEqual(prices.major_axis[0], date)

    def test_interactive_brokers_price_handler(self):
        date = dt.datetime(2016, 12, 21)
        ph = InteractiveBrokersPriceHandler()
        symbols = [Indices.sp_100_etf.value, Indices.sp_500_etf.value]
        prices = ph.request_prices(date, symbols)
        self.assertEqual(set(prices.minor_axis), set(symbols))
        self.assertEqual(prices.major_axis[0], date)


if __name__ == "__main__":
    unittest.main()
