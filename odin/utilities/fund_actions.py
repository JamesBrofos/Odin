"""Funds in Odin may need to periodically rebalance themselves or have
management fees subtracted from their total equity. Rebalancing can be performed
at a number of different time resolutions including weekly, monthly, quarterly,
and annually. Odin will determine if the corresponding number of trading days
have elapsed and then enact a rebalancing or management event if required by the
trading strategy.
"""
period_dict = {
    "weekly": 7,
    "monthly": 21,
    "quarterly": 63,
    "annually": 252
}
