import datetime as dt
import pandas as pd
from odin.utilities import params
from odin.utilities.finance import Indices


start_date = dt.datetime(2012, 1, 1)
end_date = dt.datetime(2016, 12, 21)
sell_date = dt.datetime(2016, 12, 19)
symbols = pd.Series([Indices.sp_500_etf])
init_capital = 100000.0
maximum_capacity = 1
buy_size = 100
sell_size = 50
rebalance_period = 252
manage_period = 1
n_init = 10
pid = "long"
transaction_cost = 0.0
verbosity = 1
