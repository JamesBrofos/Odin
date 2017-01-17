"""Event Verbosity Declaration Module

This module declares the verbosity level at which certain informational
statements will appear. The higher the verbosity level, the more information
will be printed to the console as shares are transacted and market data is
received.
"""
from .odin_enum import OdinEnum
from .event_types import Events

verbosity_dict = {
    # Market data events.
    Events.market: 3,
    # Portfolio-level events.
    Events.signal: 2,
    Events.order: 2,
    Events.fill: 1,
    # Fund-level events.
    Events.rebalance: 1,
    Events.management: 1,
}

class Verbosities(OdinEnum):
    portfolio = 3
