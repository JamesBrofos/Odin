from odin.portfolio import SimulatedPortfolio
from odin.utilities import params
from odin.handlers.fund_handler import FundHandler
from odin.fund import SimulatedFund
from odin.strategy.templates import BuyAndHoldStrategy
from handlers import events, dh, eh, posh, porth, posh_bench, porth_bench
from settings import rebalance_period, manage_period, start_date, verbosity, fid
from strategy import BuyTheDipStrategy, BenchmarkBuyAndHoldStrategy


# Generate objects for the portfolios and strategies that the fund will trade.
portfolios = [
    SimulatedPortfolio(dh, posh, porth),
    SimulatedPortfolio(dh, posh_bench, porth_bench),
]
strategies = [
    BuyTheDipStrategy(params.Directions.long_dir, portfolios[0]),
    BenchmarkBuyAndHoldStrategy(params.Directions.long_dir, portfolios[1]),
]
# Create the fund and fund handler objects.
fh = FundHandler(
    events, strategies, rebalance_period, manage_period, start_date, fid
)
fund = SimulatedFund(dh, eh, fh, verbosity)

