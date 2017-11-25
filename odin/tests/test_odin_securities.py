import datetime as dt
import pandas as pd
import numpy as np
import unittest
from odin_securities.queries import gets
from odin_securities.vendors import quandl


class OdinSecuritiesTest(unittest.TestCase):
    def test_get_actions(self):
        start = dt.datetime(2013, 1, 1)
        end = dt.datetime(2016, 1, 1)
        a = gets.actions(start, end)

    def test_valid_symbols(self):
        symbol = "^^^^"
        self.assertFalse(quandl.check_valid_symbol(symbol))

if __name__ == "__main__":
    unittest.main()
