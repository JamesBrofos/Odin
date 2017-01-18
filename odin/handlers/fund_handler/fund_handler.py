from odin_securities import conn
from odin_securities.queries import gets, updates, exists, inserts
from ...utilities import compute_days_elapsed
from ...events import RebalanceEvent, ManagementEvent


class FundHandler(object):
    """Fund Handler Class

    The fund handler class controls when Odin's fund objects will either
    rebalance the equity holdings of the constituent portfolios or when fund
    management events are required. These two events are controlled by detecting
    when a certain time interval (measured in days) has elapsed since the
    previous such event.
    """
    def __init__(
            self, events, strategies, rebalance_period, manage_period,
            date_entered, fund_id
    ):
        """Initialize parameters of the fund handler object."""
        self.events = events
        self.strategies = strategies
        self.portfolios = [s.portfolio for s in self.strategies]
        self.rebalance_period = rebalance_period
        self.manage_period = manage_period
        self.date_entered = date_entered
        self.fund_id = fund_id
        # Set the assets under management to be the sum of the capital
        # intitially contained in each of the constituent portfolios.
        self.aum = sum([p.portfolio_handler.capital for p in self.portfolios])

    def to_database_fund(self):
        """Insert the fund object into the Odin Securities master database.
        """
        does_not_exist = exists.fund(self.fund_id)
        if does_not_exist:
            inserts.fund(self)
        else:
            fid = gets.id_for_fund(self.fund_id)
            updates.fund(self, fid)

        conn.commit()

    @classmethod
    def from_database_fund(cls, fund_id, events, strategies):
        """Create an instance of a fund handler object using the relevant data
        from a fund database object. This is useful for preserving the state of
        a fund between trading sessions.
        """
        fund = gets.fund(fund_id).iloc[0]
        rebalance = fund["rebalance_period"]
        manage = fund["manage_period"]
        date_entered = fund["entry_date"]

        # Check that every portfolio in the strategies has the same identifier
        # as the fund.
        fund_name = fund["fund"]
        for s in strategies:
            if s.portfolio.portfolio_handler.fund_id != fund_name:
                raise ValueError(
                    "Portfolio and fund identifier mismatch:\t{}\t{}".format(
                        s.portfolio.portfolio_handler.fund_id, fund_name
                    )
                )

        return cls(events, strategies, rebalance, manage, date_entered, fund_id)

    def process_market_event(self, market_event):
        """The fund processes market data after all of the portfolios have done
        so and possibly generated signals. The fund will look for indicators to
        take action on the scale of the entire fund, which will impact each of
        the constituent portfolios.

        For instance, Odin currently implements a utility for rebalancing
        positions.
        """
        # Extract the management and rebalancing time period indicators.
        manage, rebalance = self.manage_period, self.rebalance_period
        # Compute the number of days that the fund has been trading.
        date = market_event.datetime
        n_days = compute_days_elapsed(self.date_entered, date)
        # Detect when it is time to rebalance the portfolio.
        will_rebalance = n_days % rebalance == 0 and rebalance > 1
        # Detect when it is time to take management fees from the fund.
        will_manage = n_days % manage == 0 and manage > 1

        if will_rebalance or will_manage:
            # Note that it is important and necessary to clear the events queue
            # at this stage because otherwise we have residual signal events
            # that need to be replaced by the order to rebalance positions.
            self.events.clear()
            # Close all of the positions.
            for s in self.strategies:
                s.close()

            # If we are managing.
            if will_manage:
                self.events.put(ManagementEvent(date))

            # If we are rebalancing.
            if will_rebalance:
                self.events.put(RebalanceEvent(date))

    def rebalance(self):
        """At a rebalance event, we will partition the total capital of the fund
        equally among each of the portfolios. This is done to prevent any one
        strategy from vastly outstripping the equity of the other portfolios.
        Periodic rebalancing keeps these equity levels approximately the same
        and is critical for market neutral strategies.
        """
        equity = sum([p.portfolio_handler.equity for p in self.portfolios])
        n_port = len(self.portfolios)
        for p in self.portfolios:
            p.portfolio_handler.capital = equity / n_port

    def manage(self):
        """At management events, a portion of the AUM and a portion of the gains
        earned so far are taken out as management fees for the portfolio
        manager.
        """
        # Compute the equity value of the fund and record the number of
        # portfolios being traded.
        equity = sum([p.portfolio_handler.equity for p in self.portfolios])
        n_port = len(self.portfolios)
        # Only take a cut if we've exceeded a highwater mark.
        if equity > self.aum:
            two = 0.02 * self.aum
            twenty = 0.2 * (equity - self.aum)
            post_equity = equity - two - twenty
            for p in self.portfolios:
                p.portfolio_handler.capital = post_equity / n_port

            # Reset the assets under management to be the equity earned so far.
            self.aum = post_equity
