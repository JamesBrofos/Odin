import datetime as dt
import pandas as pd
from odin.utilities import params


# Start date and end date of the time series.
start_date = dt.datetime(2006, 1, 1)
end_date = dt.datetime(2016, 12, 30)
# Only trade the S&P 500 ETF.
symbols = ["SPY"]

# Start trading will $100,000 in capital initially.
init_capital = 100000.0
# Only hold a single position.
maximum_capacity = 1

# Number of prior trading days to download at the start of the time series.
n_init = 10
# Set an identifier for the portfolio.
pid = "buy_and_hold"
fid = "fund"

# Set verbosity level.
verbosity = 1
