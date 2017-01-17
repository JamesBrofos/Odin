import os
import pickle
from odin.events import EventsQueue
from odin.handlers.portfolio_handler import PortfolioHandler
from odin.handlers.position_handler import ModernPortfolioPositionHandler
from odin.handlers.execution_handler import SimulatedExecutionHandler
from odin.handlers.symbol_handler import FixedSymbolHandler
from odin.handlers.data_handler import DatabaseDataHandler
from odin.handlers.data_handler.price_handler import DatabasePriceHandler
import settings


# Events queue for handling market data, signals, orders, and fills.
events = EventsQueue()
# Symbol handler will determine which symbols will be processed during trading.
# In this example, we will just trade the S&P 500 ETF (SPY).
sh = FixedSymbolHandler(settings.symbols)

# Set up a price handler and a data handler to provide data to the trading
# system.
dh = DatabaseDataHandler(
    events, sh, settings.start_date, settings.end_date, settings.n_init
)
# Execution handler executes trades.
eh = SimulatedExecutionHandler(dh, settings.transaction_cost)

# The position handler determines how much of the asset should be purchased
# during trading. Also create a portfolio handler to manage transactions and
# keeping track of capital.
posh_long = ModernPortfolioPositionHandler(dh, 0.4)
porth_long = PortfolioHandler(
    settings.maximum_capacity, dh, "long", settings.init_capital
)

