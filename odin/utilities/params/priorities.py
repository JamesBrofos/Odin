"""Event Priority Declaration Module

Events are prioritized according to their impact on the portfolio. Market events
are regarded as least important and fill events as the most important. One notes
that signal events have varying priority according to their trade type: Odin
prioritizes selling over buying so that liquidity can be freed up before buying
decisions are made; this allows more assets to be bought and enforces a more
active utilization of capital.
"""
from .event_types import Events
from .trade_types import TradeTypes


priority_dict = {
    Events.market: 7,
    # Portfolio-level events.
    Events.signal: {
        TradeTypes.buy_trade: 6,
        TradeTypes.sell_trade: 5,
        TradeTypes.exit_trade: 4
    },
    Events.order: 3,
    Events.fill: 2,
    # Fund-level events. Notice that management events have lower priority than
    # rebalancing events since presumably we should account for the transaction
    # fees associated with rebalancing before taking a cut.
    Events.rebalance: 8,
    Events.management: 9,
}
