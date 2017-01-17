import pandas as pd
from odin_securities.queries import gets
from .abstract_price_handler import AbstractPriceHandler
from ....utilities.params import PriceFields


class DatabasePriceHandler(AbstractPriceHandler):
    """Database Price Handler Class

    The database price handler extracts the corresponding price data from the
    requested symbols stored in the Odin Securities master database.
    """
    def request_prices(self, current_date, symbols):
        """Implementation of abstract base class method."""
        prices = gets.prices(current_date, symbols=symbols)
        prices.drop(["adj_price_close", "adj_volume"], inplace=True)
        prices.items = [
            PriceFields.current_price.value,
            PriceFields.sim_high_price.value,
            PriceFields.sim_low_price.value,
        ]
        return prices
