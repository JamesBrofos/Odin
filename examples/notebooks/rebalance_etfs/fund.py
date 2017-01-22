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
    SimulatedPortfolio(handlers.dh, handlers.posh_bench, handlers.porth_bench),
]
strategies = [
    strategy.RebalanceETFStrategy(portfolios[0], params.Directions.long_dir),
    strategy.BuyAndHoldSpyderStrategy(portfolios[1], params.Directions.long_dir),
]
# Create the fund and fund handler objects.
fh = FundHandler(
    handlers.events, strategies, settings.start_date, settings.fid
)
fund = SimulatedFund(handlers.dh, handlers.eh, fh, settings.verbosity)

