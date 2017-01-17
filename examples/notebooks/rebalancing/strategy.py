import pandas as pd
from odin.strategy import AbstractStrategy


class RebalanceDemoStrategy(AbstractStrategy):
    """Rebalance Demo Strategy Class
    """
    def buy_indicator(self, feats):
        """Implementation of abstract base class method."""
        return True

    def sell_indicator(self, feats):
        """Implementation of abstract base class method."""
        date = self.portfolio.data_handler.current_date
        ph = self.portfolio.portfolio_handler
        days_held = ph.filled_positions[
            feats.name
        ].compute_holding_period(date).days
        
        return days_held > 62

    def exit_indicator(self, feats):
        """Implementation of abstract base class method."""
        return False

    def generate_features(self):
        """Implementation of abstract base class method."""
        symbols = self.portfolio.data_handler.bars.ix[
            "adj_price_open", -1, :
        ].dropna().index
        return pd.DataFrame(index=symbols)

    def generate_priority(self, feats):
        """Implementation of abstract base class method."""
        return self.portfolio.data_handler.bars.ix[
            "adj_price_open", -1, :
        ].dropna().index
