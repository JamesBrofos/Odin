"""Interactive Brokers Parameters

This mdoule specifies parameters that are required to connect to the Interactive
Brokers (IB) Trader Workstation. In particular, we specify here the port that
listens for connections from the IB API. We also specify the global identifier
for submitting trades to be executed and the identifier for retrieving
information specific to a portfolio.

This file contains privileged account information for both the live trading
account and the paper trading account. These are required for submitting trades
in their respective trading environments.
"""
from .odin_enum import OdinEnum


class InteractiveBrokers(OdinEnum):
    # Client identifiers for connections to Interactive Brokers.
    portfolio_id = 101
    execution_handler_id = 102
    data_handler_id = 103
    # Interactive Brokers port connection.
    port = 7497


def ib_commission(quantity, price):
    """Compute the commission charged by Interactive Brokers."""
    c = 0.005 * quantity
    maximum =  0.005 * quantity * price
    minimum = 1.0

    if c < minimum:
        # The commission may not be less than one dollar.
        c = minimum
    elif c > maximum:
        # The commission may not exceed more than 0.005% of the total value of
        # the position.
        c = maximum

    return c


# Define a list of error codes that are silent.
ib_silent_errors = set([
    # HMDS data farm connection is OK:ushmds.
    2106,
    # Market data farm connection is OK:usfarm.
    2104,
])
