import unittest
import datetime as dt
from odin.handlers.position_handler.position import FilledPosition
from odin.utilities import params

class TestPosition(unittest.TestCase):
    def test_to_database_position(self):
        s = "SPY"
        q = 100
        d = params.Directions.long_dir
        t = params.TradeTypes.buy_trade
        a = params.action_dict[(d, t)]
        pid = "test_portfolio_id"
        date = dt.datetime.today()
        price = 100.0
        update_price = 101.0
        pos = FilledPosition(s, q, d, t, pid, date, price)
        pos.transact_shares(a, q, price)
        pos.to_database_position()

    def test_from_database_position(self):
        s = "SPY"
        pid = "test_portfolio_id"
        pos = FilledPosition.from_database_position(pid, s)
        self.assertEqual(pos.avg_price, 100.01)
        self.assertEqual(pos.portfolio_id, pid)
        self.assertEqual(pos.quantity, 100)
        self.assertEqual(pos.direction, params.Directions.long_dir)
        self.assertEqual(pos.trade_type, params.TradeTypes.buy_trade)

    def test_long_position(self):
        s = "GOOG"
        q = 100
        d = params.Directions.long_dir
        t = params.TradeTypes.buy_trade
        a = params.action_dict[(d, t)]
        pid = "test_portfolio_id"
        date = dt.datetime.today()
        price = 100.0
        update_price = 101.0
        pos = FilledPosition(s, q, d, t, pid, date, price)
        pos.transact_shares(a, q, price)
        pos.update_market_value(update_price)
        self.assertEqual(
            pos.percent_pnl,
            1 + (pos.market_value - pos.cost_basis) / pos.cost_basis
        )
        self.assertEqual(pos.quantity, q)
        self.assertEqual(pos.market_value, 10100.0)
        self.assertEqual(pos.unrealized_pnl, 99.0)
        self.assertEqual(pos.tot_commission, 1.0)

        sell_price = 100.5
        pos.transact_shares(params.Actions.sell, q // 2, sell_price)
        self.assertEqual(pos.quantity, q // 2)
        self.assertEqual(pos.realized_pnl, 48.0)
        self.assertEqual(pos.unrealized_pnl, 24.5)
        self.assertEqual(pos.tot_commission, 2.0)

        sell_price = 101.0
        pos.transact_shares(params.Actions.sell, q // 2, sell_price)
        self.assertEqual(pos.quantity, 0)
        self.assertEqual(pos.realized_pnl, 72.0)
        self.assertEqual(pos.unrealized_pnl, 0.)
        self.assertEqual(pos.tot_commission, 3.0)

    def test_short_position(self):
        s = "GOOG"
        q = 100
        d = params.Directions.short_dir
        t = params.TradeTypes.buy_trade
        a = params.action_dict[(d, t)]
        pid = "test_portfolio_id"
        date = dt.datetime.today()
        price = 100.0
        update_price = 101.0
        pos = FilledPosition(s, q, d, t, pid, date, price)
        pos.transact_shares(a, q, price)
        pos.update_market_value(update_price)
        self.assertEqual(
            pos.percent_pnl,
            1 - (pos.market_value - pos.cost_basis) / pos.cost_basis
        )
        self.assertEqual(pos.quantity, q)
        self.assertEqual(pos.market_value, -10100.0)
        self.assertEqual(pos.unrealized_pnl, -101.0)
        self.assertEqual(pos.tot_commission, 1.0)

        buy_price = 100.5
        pos.transact_shares(params.Actions.buy, q // 2, buy_price)
        self.assertEqual(pos.quantity, q // 2)
        self.assertEqual(pos.realized_pnl, -52.0)
        self.assertEqual(pos.unrealized_pnl, -25.5)
        self.assertEqual(pos.tot_commission, 2.0)

        buy_price = 101.0
        pos.transact_shares(params.Actions.buy, q // 2, buy_price)
        self.assertEqual(pos.quantity, 0)
        self.assertEqual(pos.realized_pnl, -78.0)
        self.assertEqual(pos.unrealized_pnl, 0.)
        self.assertEqual(pos.tot_commission, 3.0)


if __name__ == "__main__":
    unittest.main()

