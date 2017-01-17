import unittest
import datetime as dt
from odin.handlers.execution_handler import SimulatedExecutionHandler
from odin.handlers.data_handler import DatabaseDataHandler
from odin.handlers.symbol_handler import FixedSymbolHandler
from odin.handlers.data_handler.price_handler import DatabasePriceHandler
from odin.events import EventsQueue, MarketEvent, FillEvent, OrderEvent
from odin.utilities.params import TradeTypes, Directions, PriceFields

class ExecutionHandlerTest(unittest.TestCase):
    def test_simulated_execution_handler(self):
        """Ensures that the simulated execution handler is processing order
        events in the expected way.
        """
        q = EventsQueue()
        symbol = "SPY"
        sh = FixedSymbolHandler([symbol])
        start, end = dt.datetime(2015, 1, 2), dt.datetime(2015, 1, 9)
        dh = DatabaseDataHandler(q, sh, start, end, 10)
        dh.request_prices()
        eh = SimulatedExecutionHandler(dh)
        quantity = 100
        o = OrderEvent(
            symbol, quantity, TradeTypes.buy_trade, Directions.long_dir,
            start, "long"
        )
        eh.execute_order(o)
        dh.update()
        f = q.get()
        price_id = [
            PriceFields.sim_low_price.value, PriceFields.sim_high_price.value
        ]
        price = dh.prices.ix[price_id, 0, symbol].mean()
        fill_cost = price * quantity * (1.0 + eh.transaction_cost)
        self.assertTrue(type(f) == FillEvent)
        self.assertTrue(type(q.get()) == MarketEvent)
        self.assertTrue(q.empty())
        self.assertEqual(fill_cost, f.fill_cost)


if __name__ == "__main__":
    unittest.main()
