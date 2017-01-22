from odin.portfolio import InteractiveBrokersPortfolio
from odin.utilities import params
from odin.handlers.fund_handler import FundHandler
from odin.fund import Fund
from odin.strategy.templates import BuyAndHoldStrategy
from odin_securities.queries import exists
import handlers
import settings

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
    BuyAndHoldStrategy(
        portfolios[0], params.Directions.long_dir
    ),
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

