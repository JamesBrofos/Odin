import datetime as dt
import pandas as pd
from odin.utilities import params
from odin.utilities.finance import Indices


# Start date and end date of the time series.
start_date = dt.datetime(2006, 1, 1)
end_date = dt.datetime(2016, 12, 30)
# Trade ETFs.
symbols = ["SPY", "AGG"]
weights = {"SPY": 0.6, "AGG": 0.4}

# Start trading will $100,000 in capital initially.
init_capital = 100000.0
# Only hold a single position.
maximum_capacity = 2

# Number of prior trading days to download at the start of the time series.
n_init = 10
# Set an identifier for the portfolio.
pid = "weighted_etfs"
pid_bench = "spyder_etf"
fid = "fund"
# Assume that transacting shares moves the price by five-hundredths of a basis
# point.
transaction_cost = 0.0005

# Set verbosity level.
verbosity = 1
