import os
import pickle
from odin.events import EventsQueue
from odin.handlers.portfolio_handler import PortfolioHandler
from odin.handlers.position_handler import EqualEquityPositionHandler
from odin.handlers.execution_handler import InteractiveBrokersExecutionHandler
from odin.handlers.symbol_handler import FixedSymbolHandler
from odin.handlers.data_handler import InteractiveBrokersDataHandler
from odin.handlers.data_handler.price_handler import (
    InteractiveBrokersPriceHandler
)
from odin_securities.queries import exists
import settings


# Create a portfolio handler to manage transactions and keeping track of
# capital.
if exists.portfolio(settings.pid):
    porth = PortfolioHandler.from_database_portfolio(settings.pid)
else:
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
dh = InteractiveBrokersDataHandler(events, sh, settings.n_init)
# Execution handler executes trades.
eh = InteractiveBrokersExecutionHandler(events)

# Position handler to determine how much of an asset to purchase.
posh = EqualEquityPositionHandler(settings.maximum_capacity, dh)
