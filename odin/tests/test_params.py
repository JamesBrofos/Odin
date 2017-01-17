import unittest
from odin.utilities.params import Events, priority_dict, TradeTypes


class ParamsTest(unittest.TestCase):
    def test_priorities(self):
        """Test to ensure that the relative importance of portfolio-level events
        are consistent.
        """
        me = priority_dict[Events.market]
        se = priority_dict[Events.signal]
        oe = priority_dict[Events.order]
        fe = priority_dict[Events.fill]
        self.assertTrue(me > se[TradeTypes.buy_trade])
        self.assertTrue(se[TradeTypes.buy_trade] > se[TradeTypes.sell_trade])
        self.assertTrue(se[TradeTypes.sell_trade] > se[TradeTypes.exit_trade])
        self.assertTrue(se[TradeTypes.exit_trade] > oe)
        self.assertTrue(oe > fe)


if __name__ == "__main__":
    unittest.main()
