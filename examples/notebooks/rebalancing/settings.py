import datetime as dt
import pandas as pd
from odin.utilities import params
from odin.utilities.finance import Indices


# Start date and end date of the time series.
start_date = dt.datetime(2012, 1, 1)
end_date = dt.datetime(2016, 12, 21)
sell_date = dt.datetime(2016, 12, 19)
# Only trade the S&P 500 ETF.
symbols = [Indices.sp_500_etf]

# Start trading will $100,000 in capital initially.
init_capital = 100000.0
# Only hold a single position and set limits on how many shares are transacted.
maximum_capacity = 1
buy_size = 100
sell_size = 50
rebalance_period = 252
manage_period = 1
# Number of prior trading days to download at the start of the time series.
n_init = 10

# Set an identifier for the portfolio.
long_pid = "long_rebalancing"
short_pid = "short_rebalancing"
fid = "fund"

# Assume that transacting shares moves the price by five-hundredths of a basis
# point.
transaction_cost = 0.0

# Set the verbosity level.
verbosity = 1
