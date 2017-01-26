import os
import pickle
from odin.events import EventsQueue
from odin.handlers.portfolio_handler import PortfolioHandler
from odin.handlers.position_handler.templates import (
    SuggestedProportionPositionHandler
)
from odin.handlers.execution_handler import SimulatedExecutionHandler
from odin.handlers.symbol_handler import FixedSymbolHandler
from odin.handlers.data_handler import DatabaseDataHandler
from odin.handlers.data_handler.price_handler import DatabasePriceHandler
import settings


# Create a portfolio handler to manage transactions and keeping track of
# capital.
porth = PortfolioHandler(
    settings.maximum_capacity, settings.pid, settings.init_capital,
    settings.fid
)

# Events queue for handling market data, signals, orders, and fills.
events = EventsQueue()
# Symbol handler will determine which symbols will be processed during trading.
# In this example, we will just trade the S&P 500 ETF (SPY).
sh = FixedSymbolHandler(settings.symbols, [porth])

# Set up a price handler and a data handler to provide data to the trading
# system.
dh = DatabaseDataHandler(
    events, sh, settings.start_date, settings.end_date, settings.n_init
)
# Execution handler executes trades.
eh = SimulatedExecutionHandler(dh, settings.transaction_cost)

# Position handler to determine how much of an asset to purchase.
posh = SuggestedProportionPositionHandler(dh)
