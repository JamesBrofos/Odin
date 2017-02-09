import pandas as pd
from ....strategy import AbstractStrategy


class DefaultFeaturesMixin(AbstractStrategy):
    """Default Features Mixin Class

    This just creates an empty dataframe containing as the index the symbols
    available on each day of trading and no columns.
    """
    def generate_features(self):
        """Implementation of abstract base class method."""
        symbols = self.portfolio.data_handler.bars.ix[
            "adj_price_close", -1, :
        ].dropna().index
        return pd.DataFrame(index=symbols)
