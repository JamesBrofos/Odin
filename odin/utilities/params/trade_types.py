"""Trade Type Declaration Module

Odin conceptualizes entering either a long or short position as a 'BUY'
operation. This is done so that taking a short position can be regarded as
setting aside equity to cover the cost of the initial position and that this is
not fundamentally different from using equity to purchase shares in a long
position.

The different kinds of trade types are 'BUY', 'SELL', and 'EXIT'. The first two
are self-explanatory. The third corresponds to the idea of completely
liquidating a position (either long or short) buy selling shares (for longs) or
buying shares (for shorts). A 'SELL' signal where the number of shares equals
the total number of shares held is equivalent to an exit.
"""
from .odin_enum import OdinEnum


class TradeTypes(OdinEnum):
    buy_trade = "BUY"
    sell_trade = "SELL"
    exit_trade = "EXIT"

