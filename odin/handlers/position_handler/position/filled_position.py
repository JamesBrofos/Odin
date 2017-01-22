import datetime as dt
import numpy as np
import pandas as pd
from odin_securities import conn
# from odin_securities.utilities import get_id_for_symbol, get_id_for_portfolio
from odin_securities.queries import gets, inserts, updates, exists
from .pending_position import PendingPosition
from ....utilities import compute_days_elapsed
from ....utilities.params import (
    Directions, Actions, IB, TradeTypes, ib_commission
)


class FilledPosition(PendingPosition):
    """Filled Position Class

    The position object represents a position held by a portfolio object. It
    captures how much of the position is held, whether or not the position is
    long or short, the profit-and-loss on the position at the current time
    period, and the ticker symbol associated with the underlying asset.
    """
    def __init__(
            self,
            symbol,
            direction,
            trade_type,
            portfolio_id,
            date_entered,
            avg_price,
            buys=0,
            sells=0,
            avg_buys_price=0.0,
            avg_sells_price=0.0,
            tot_commission=0.0
    ):
        """Initialize parameters of the position object."""
        super(FilledPosition, self).__init__(
            symbol, direction, trade_type, portfolio_id
        )
        self.date_entered = date_entered

        # Profit and loss.
        self.unrealized_pnl, self.realized_pnl = 0.0, 0.0
        self.market_value = 0.0

        # Number of buys and sells.
        self.buys, self.sells = buys, sells
        self.net = self.buys - self.sells
        self.quantity = abs(self.net)
        # Price of buys and sells on average.
        self.avg_price = avg_price
        self.cost_basis = self.net * self.avg_price
        self.avg_buys_price = avg_buys_price
        self.avg_sells_price = avg_sells_price
        self.tot_buys_price = self.buys * self.avg_buys_price
        self.tot_sells_price = self.sells * self.avg_sells_price
        # Keep track of total commission costs.
        self.tot_commission = tot_commission
        self.net_tot = self.tot_sells_price - self.tot_buys_price
        self.net_tot_incl_comm = self.net_tot - self.tot_commission

    def __str__(self):
        """String representation of the filled position object."""
        return "{}\t{}\t{:0.2f}\t{:0.4f}".format(
            self.symbol, self.date_entered.date(), self.relative_value,
            self.percent_pnl
        )

    def transact_shares(self, action, quantity, price):
        """Depending upon whether the action was a buy or sell calculate the
        average bought cost, the total bought cost, the average price and the
        cost basis. Finally, calculate the net total without commission.
        """
        # Record the total commission costs for this position so far.
        commission = ib_commission(quantity, price)
        self.tot_commission += commission
        # Compute the value of the shares being transacted.
        value = price * quantity

        # Adjust total bought and sold.
        if action == Actions.buy:
            # Number of shares transacted.
            n_transacted = self.buys + quantity
            # If shares are bought, then recompute the average cost of buying
            # the shares, accounting for shares already held.
            self.avg_buys_price = (
                self.avg_buys_price * self.buys + value
            ) / n_transacted

            if self.action != Actions.sell:
                self.avg_price = (
                    self.avg_price * self.buys + value + commission
                ) / n_transacted

            # Increment quantity bought.
            self.buys += quantity
            self.tot_buys_price = self.buys * self.avg_buys_price
        elif action == Actions.sell:
            # Number of shares transacted.
            n_transacted = self.sells + quantity
            # If shares are being sold (even on margin), then recompute the
            # average price of selling the shares, accounting for shares already
            # sold.
            self.avg_sells_price = (
                self.avg_sells_price * self.sells + value
            ) / n_transacted

            if self.action != Actions.buy:
                self.avg_price = (
                    self.avg_price * self.sells + value - commission
                ) / n_transacted

            # Increment quantity sold.
            self.sells += quantity
            self.tot_sells_price = self.sells * self.avg_sells_price

        else:
            raise ValueError(
                "Invalid action passed to transact shares: {}".format(action)
            )

        # Record the new number of shares bought or sold. Also compute the net
        # value accounting for shares bought and sold.
        self.net = self.buys - self.sells
        self.quantity = abs(self.net)
        self.net_tot = self.tot_sells_price - self.tot_buys_price
        self.net_tot_incl_comm = self.net_tot - self.tot_commission
        # Compute the cost basis.
        self.cost_basis = self.net * self.avg_price
        # Update market value.
        self.update_market_value(price)

    def update_market_value(self, price):
        """Compute the current marke value of the position. This is the current
        price multiplied by the direction of the trade (r2epresented by the sign
        of the net number of shares bought and sold). The function also updated
        the unrealized and realized profits and losses.
        """
        # Compute the mean of the bid and ask price to compute the assumed value
        # of the position.
        #
        # N.B. That the market value is akin to the amount of cash that is would
        # be injected into the portfolio if the position were liquidated. This
        # means that if a position is short, then a negative amount will be
        # injected (i.e. paid out). On the other hand, the current value is the
        # profit-and-loss on a position relative to the cost basis.
        self.market_value = self.net * price
        self.unrealized_pnl = self.market_value - self.cost_basis
        self.realized_pnl = self.market_value + self.net_tot_incl_comm

    def compute_holding_period(self, current_date):
        """Compute the time period over which the position has been held. This
        is simply the temporal difference between when the position was entered
        (which is recorded on creation of a position) and the current time.

        Unlike previous methods that only computed the days held in terms of
        days elapsed, this method also accounts for finer-grain temporal
        differences.
        """
        delta_seconds = 86400 - (self.date_entered - current_date).seconds
        delta_days = compute_days_elapsed(self.date_entered, current_date)
        if self.date_entered.time() > dt.time(0, 0):
            delta_days -= 1

        return dt.timedelta(days=delta_days, seconds=delta_seconds)

    def to_database_position(self):
        """Write the position to the database. This allows the position to be
        persistent across trading sessions.
        """
        # Get identifiers for both the stock symbol and the portfolio.
        pid = gets.id_for_portfolio(self.portfolio_id)
        sid = gets.id_for_symbol(self.symbol)
        does_exist = exists.position(sid, pid)
        # Insert the position into the database.
        if not does_exist:
            inserts.position(self, sid, pid)
        else:
            updates.position(self, sid, pid)

        # Commit changes to the database.
        conn.commit()

    @property
    def percent_pnl(self):
        """Computes the profit-and-loss on a position. This is the percentage
        difference of the current price relative to the average price of the
        asset added to or subtracted from unity according to whether or not the
        position is long or short the asset.
        """
        if self.net == 0:
            raise ValueError(
                "Percentage profit and loss is not defined for positions with "
                "no holdings."
            )
        else:
            ret = self.unrealized_pnl / self.cost_basis * np.sign(self.net)
            return 1.0 + ret

    @property
    def relative_value(self):
        """Compute the relative value of the position. This is the cost basis
        multiplied by the profit-and-loss since entering the position.
        """
        return abs(self.cost_basis * self.percent_pnl)

    @classmethod
    def from_database_position(cls, portfolio_id, symbol):
        """Create an instance of a filled position object using the relevant
        data stored in the Odin Securities master database.
        """
        # Get the identifiers for both the portfolio and the symbol.
        pid = gets.id_for_portfolio(portfolio_id)
        sid = gets.id_for_symbol(symbol)
        qry = """
        SELECT * FROM positions WHERE symbol_id={} AND portfolio_id={}
        """.format(sid, pid)
        rec = pd.read_sql(qry, conn, index_col=["id"]).iloc[0]
        # Extract variables.
        date_entered = rec["date_entered"]
        avg_price = float(rec["avg_price"])
        buys, sells = int(rec["buys"]), int(rec["sells"])
        avg_buys_price = float(rec["avg_buys_price"])
        avg_sells_price = float(rec["avg_sells_price"])
        tot_commission = float(rec["tot_commission"])
        direction = Directions(rec["direction"])
        trade_type = TradeTypes(rec["trade_type"])
        # Return a filled position object populated from the database.
        return cls(
            symbol,
            direction,
            trade_type,
            portfolio_id,
            date_entered,
            avg_price,
            buys,
            sells,
            avg_buys_price,
            avg_sells_price,
            tot_commission
        )

    @classmethod
    def from_pending_position(cls, pending, date, price):
        """Create an instance of a filled position object using the relevant
        data stored in a pending position object.
        """
        return cls(
            pending.symbol,
            pending.direction,
            pending.trade_type,
            pending.portfolio_id,
            date,
            price,
        )

