from .odin_enum import OdinEnum


class Events(OdinEnum):
    """Event Type Enumeration

    Odin trades by awaiting sequences of predetermined events and interpreting
    such events in order to make subsequent decisions. The documentation for
    each event type is contained in the events module, though string identifiers
    are stored in this file for global access.

    There are two kinds of indicators: The first operates at the portfolio level
    and is interpreted by a specific portfolio object; the second is for the
    larger level of funds, impacting all of the portfolio objects contained
    within a fund object.
    """
    # New market data event.
    market = "MARKET"
    # Portfolio-level indicators.
    signal = "SIGNAL"
    order = "ORDER"
    fill = "FILL"
    # Fund-level events.
    rebalance = "REBALANCE"
    management = "MANAGEMENT"
