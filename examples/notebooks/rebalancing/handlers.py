import os
import pickle
from odin.events import EventsQueue
from odin.handlers.portfolio_handler import PortfolioHandler
from odin.handlers.position_handler import FixedPositionHandler
from odin.handlers.execution_handler import SimulatedExecutionHandler
from odin.handlers.symbol_handler import FixedSymbolHandler
from odin.handlers.data_handler import DatabaseDataHandler
from odin.handlers.data_handler.price_handler import DatabasePriceHandler
import settings


events = EventsQueue()
sh = FixedSymbolHandler(["SPY"])
dh = DatabaseDataHandler(
    events, sh, settings.start_date, settings.end_date, settings.n_init
)
eh = SimulatedExecutionHandler(dh, settings.transaction_cost)
posh_long = FixedPositionHandler(settings.buy_size, settings.sell_size)
posh_short = FixedPositionHandler(settings.buy_size, settings.sell_size)
porth_long = PortfolioHandler(
    settings.maximum_capacity, dh, settings.long_pid, settings.init_capital,
    settings.fid
)
porth_short = PortfolioHandler(
    settings.maximum_capacity, dh, settings.short_pid, settings.init_capital,
    settings.fid
)

