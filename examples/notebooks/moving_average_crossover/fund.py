from odin.portfolio import SimulatedPortfolio
from odin.utilities import params
from odin.handlers.fund_handler import FundHandler
from odin.fund import SimulatedFund
from odin.strategy.templates import BuyAndHoldStrategy
import strategy
import settings
import handlers


# Generate objects for the portfolios and strategies that the fund will trade.
portfolios = [
    SimulatedPortfolio(handlers.dh, handlers.posh, handlers.porth),
]
strategies = [
    strategy.MovingAverageCrossoverStrategy(portfolios[0]),
]

# Create the fund and fund handler objects.
fh = FundHandler(
    handlers.events, strategies, settings.start_date, settings.fid
)
fund = SimulatedFund(handlers.dh, handlers.eh, fh, settings.verbosity)

