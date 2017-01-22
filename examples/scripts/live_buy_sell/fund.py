from odin.portfolio import InteractiveBrokersPortfolio
from odin.utilities import params
from odin.handlers.fund_handler import FundHandler
from odin.fund import Fund
from odin_securities.queries import exists
import handlers
import settings
import strategy

# Generate objects for the portfolios and strategies that the fund will trade.
portfolios = [
    InteractiveBrokersPortfolio(
        handlers.dh,
        handlers.posh,
        handlers.porth,
        settings.account
    ),
]
strategies = [
    strategy.BuySellStrategy(portfolios[0]),
]

# Create the fund and fund handler objects.
if exists.fund(settings.fid):
    fh = FundHandler.from_database_fund(
        settings.fid,
        handlers.events,
        strategies
    )
else:
    fh = FundHandler(
        handlers.events,
        strategies,
        settings.start_date,
        settings.fid
    )
    fh.to_database_fund()

fund = Fund(
    handlers.dh,
    handlers.eh,
    fh,
    settings.delay,
    settings.verbosity
)

