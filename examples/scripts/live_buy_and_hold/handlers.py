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


# Events queue for handling market data, signals, orders, and fills.
events = EventsQueue()
# Symbol handler will determine which symbols will be processed during trading.
# In this example, we will just trade the S&P 500 ETF (SPY).
sh = FixedSymbolHandler(settings.symbols)

# Set up a price handler and a data handler to provide data to the trading
# system.
dh = InteractiveBrokersDataHandler(events, sh, settings.n_init)
# Execution handler executes trades.
eh = InteractiveBrokersExecutionHandler(events)

# The position handler determines how much of the asset should be purchased
# during trading. Also create a portfolio handler to manage transactions and
# keeping track of capital.
posh_long = EqualEquityPositionHandler(settings.maximum_capacity, dh)
long_pid = "long_buy_and_hold_example"
if not exists.portfolio(long_pid):
    porth_long = PortfolioHandler.from_database_portfolio(long_pid, dh)
else:
    porth_long = PortfolioHandler(
        settings.maximum_capacity, dh, long_pid, settings.init_capital
    )

