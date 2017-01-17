import pandas as pd
from odin.strategy import AbstractStrategy
from odin.strategy.templates import BuyAndHoldStrategy
from odin.utilities.finance import Indices


class BenchmarkBuyAndHoldStrategy(BuyAndHoldStrategy):
    """Benchmark Buy And Hold Strategy Class"""
    def buy_indicator(self, feats):
        """Only buy the S&P 500 ETF"""
        return feats.name == Indices.sp_500_etf.value


class BuyTheDipStrategy(AbstractStrategy):
    """Buy The Dip Strategy Class

    This strategy will attempt to buy assets at a bargain price in the
    expectation that they will recover their value.
    """
    def buy_indicator(self, feats):
        """Implementation of abstract base class method."""
        return feats["rets"] < 0.98

    def sell_indicator(self, feats):
        """Implementation of abstract base class method."""
        return False

    def exit_indicator(self, feats):
        """Implementation of abstract base class method."""
        date = self.portfolio.data_handler.current_date
        pos = self.portfolio.portfolio_handler.filled_positions[feats.name]
        pnl = pos.percent_pnl
        days = pos.compute_holding_period(date)
        return pnl > 1.05

    def generate_features(self):
        """Implementation of abstract base class method."""
        bars = self.portfolio.data_handler.bars.ix[:, -2:, :]
        prices = self.portfolio.data_handler.prices
        feats = pd.DataFrame(index=bars.minor_axis)
        idx = "adj_price_close"
        feats["rets"] = 1.0 + (
            (bars.ix[idx, -1, :] - bars.ix[idx, -2, :]) / bars.ix[idx, -2, :]
        )

        return feats

    def generate_priority(self, feats):
        """Implementation of abstract base class method."""
        return self.portfolio.data_handler.bars.ix[
            "adj_price_open", -1, :
        ].dropna().index
