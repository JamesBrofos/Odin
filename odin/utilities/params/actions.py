"""Action Declaration Module

Because Odin uses a notion of buying for entering either long or short
positions, it is necessary to resolve combinations of directionality and trade
type to specific actions.
"""
from .direction_types import Directions
from .trade_types import TradeTypes
from .odin_enum import OdinEnum


class Actions(OdinEnum):
    buy = "BUY"
    sell = "SELL"

action_dict = {
    (Directions.long_dir, TradeTypes.buy_trade): Actions.buy,
    (Directions.long_dir, TradeTypes.sell_trade): Actions.sell,
    (Directions.short_dir, TradeTypes.buy_trade): Actions.sell,
    (Directions.short_dir, TradeTypes.sell_trade): Actions.buy,
    (Directions.long_dir, TradeTypes.exit_trade): Actions.sell,
    (Directions.short_dir, TradeTypes.exit_trade): Actions.buy,
}
