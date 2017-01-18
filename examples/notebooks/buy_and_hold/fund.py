from odin.portfolio import SimulatedPortfolio
from odin.utilities import params
from odin.handlers.fund_handler import FundHandler
from odin.fund import SimulatedFund
from odin.strategy.templates import BuyAndHoldStrategy
from handlers import events, dh, eh, posh_long, porth_long
from settings import rebalance_period, manage_period, start_date, verbosity, fid


# Generate objects for the portfolios and strategies that the fund will trade.
portfolios = [
    SimulatedPortfolio(dh, posh_long, porth_long),
]
strategies = [
    BuyAndHoldStrategy(params.Directions.long_dir, portfolios[0]),
]
# Create the fund and fund handler objects.
fh = FundHandler(
    events, strategies, rebalance_period, manage_period, start_date, fid
)
fund = SimulatedFund(dh, eh, fh, verbosity)

