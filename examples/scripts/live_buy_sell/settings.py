import datetime as dt
import pandas as pd
from odin.utilities import params
from odin.utilities.finance import Indices


# Start date and end date of the time series.
start_date = end_date = dt.datetime.today()
# Only trade the S&P 500 ETF.
symbols = [Indices.sp_500_etf.value]

# Start trading will $100,000 in capital initially.
init_capital = 100000.0
# Only hold a single position.
maximum_capacity = 1

# Account and fund identifiers.
pid = "buy_and_hold_example_portfolio"
fid = "buy_and_hold_example_fund"

# Number of prior trading days to download at the start of the time series.
n_init = 10
# Set an account for the portfolio.
account = "<YOUR IB PAPER TRADING ID>"

# The amount of time to wait before requesting more market data.
delay = 10
# Set verbosity level.
verbosity = 3
