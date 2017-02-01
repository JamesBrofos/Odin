import pandas as pd
from abc import ABCMeta, abstractmethod
from ..events import SignalEvent
from ..utilities.params import TradeTypes


class AbstractStrategy(object):
    """Abstract Strategy Class

    Strategy is an abstract base class providing an interface for all subsequent
    (inherited) strategy handling objects.

    The goal of a (derived) Strategy object is to generate signal events for
    particular symbols based on bar data streamed from a data handler object.
    This is designed to work both with historic and live data as the strategy
    object is agnostic to the data source (it obtains the bar data from a queue
    object).
    """
    __metaclass__ = ABCMeta

    def __init__(self, portfolio):
        """Initialize parameters of the abstract strategy object."""
        self.portfolio = portfolio

    def generate_signals(self):
        """This function is called to handle all of the processing of buy, sell,
        and exit signals whenever a new bar is streamed. The algorithm makes it
        impossible for an asset that has already been purchased to be purchased
        again; hence, positions that have entered into are only eligible to be
        sold off or exited.
        """
        # Get salient trading features.
        feats = self.generate_features()
        # Assign convenience variables that are constant across all elements of
        # the signal generating function.
        date = self.portfolio.data_handler.current_date
        # d = self.direction
        pid = self.portfolio.portfolio_handler.portfolio_id
        events = self.portfolio.data_handler.events
        ph = self.portfolio.portfolio_handler

        # Iterate over the underlying assets in the data handler. For those
        # assets that do not yet have an associated position in the portfolio,
        # consider them for purchase; otherwise, consider the position for
        # liquidation. The order that the assets are considered in is generated
        # by a user-specified priority.
        for stock in self.generate_priority(feats):
            stock_feat = feats.ix[stock]
            if stock in ph.filled_positions:
                # Process assets that are already held as positions.
                sell_trade_indicator = True
                if self.sell_indicator(stock_feat):
                    # Selling a position. We determine the fraction of the
                    # position that should be liquidated.
                    trade_type = TradeTypes.sell_trade
                    prop = self.compute_sell_proportion(stock_feat)
                elif self.exit_indicator(stock_feat):
                    # Exiting a position entirely; hence, the fraction of the
                    # position to sell is unity.
                    trade_type = TradeTypes.exit_trade
                    prop = 1.0
                else:
                    sell_trade_indicator = False

                if sell_trade_indicator:
                    direction = ph.filled_positions[stock].direction
                    signal_event = SignalEvent(
                        stock, prop, trade_type, direction, date, pid
                    )
                    events.put(signal_event)
            else:
                # Process assets that are candidates to become new positions.
                if self.buy_indicator(stock_feat):
                    direction = self.compute_direction(stock_feat)
                    prop = self.compute_buy_proportion(stock_feat)
                    signal_event = SignalEvent(
                        stock, prop, TradeTypes.buy_trade, direction, date, pid
                    )
                    events.put(signal_event)

    def close(self):
        """This function issues signal events that exit every position held by
        the portfolio.
        """
        # Extract the current date.
        date = self.portfolio.data_handler.current_date
        # Iterate over the positions of the portfolio and generate an exit
        # signal for that position.
        for pos in self.portfolio.portfolio_handler.filled_positions.values():
            signal_event = SignalEvent(
                pos.symbol, 1.0, TradeTypes.exit_trade, pos.direction, date,
                self.portfolio.portfolio_handler.portfolio_id
            )
            self.portfolio.data_handler.events.put(signal_event)

    @abstractmethod
    def compute_direction(self, feats):
        """Indicator of which direction (long or short) the strategy to trade a
        specific asset.
        """
        raise NotImplementedError()

    @abstractmethod
    def compute_buy_proportion(self, feats):
        """Determine the recommended proportion of capital to allocate toward
        this position. This proportion will either be heeded or modified by the
        position handler object for the associated portfolio.
        """
        raise NotImplementedError()

    @abstractmethod
    def compute_sell_proportion(self, feats):
        """Similar to the function that computes the proportion of equity to
        invest in a position, this function computes the proportions of an
        existing position to liquidate.
        """
        raise NotImplementedError()

    @abstractmethod
    def buy_indicator(self, feats):
        """Indicator function that the strategy should buy into a position."""
        raise NotImplementedError()

    @abstractmethod
    def sell_indicator(self, feats):
        """Indicator function that the strategy should sell from a position."""
        raise NotImplementedError()

    @abstractmethod
    def exit_indicator(self, feats):
        """Indicator function that the strategy should exit a position."""
        raise NotImplementedError()

    @abstractmethod
    def generate_features(self):
        """Generates salient features for constructing trading signals for
        either buying into a position or selling from it.
        """
        raise NotImplementedError()

    @abstractmethod
    def generate_priority(self, feats):
        """Generates an order in which to consider stocks. Since the portfolio
        has limited capacity, trading decisions for entering a position need to
        be prioritized.
        """
        raise NotImplementedError()
