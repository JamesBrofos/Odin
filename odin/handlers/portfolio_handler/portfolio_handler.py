import pandas as pd
import datetime as dt
from odin_securities import conn
from odin_securities.queries import gets, exists, updates, inserts, deletes
from ..position_handler.position import PendingPosition, FilledPosition
from ...portfolio.components import PortfolioState
from ...utilities.mixins import EquityMixin
from ...utilities.params import TradeTypes, action_dict, Directions


class PortfolioHandler(EquityMixin):
    """Portfolio Handler Class

    The portfolio handler class is responsible for the book-keeping relating to
    transactions of assets when the strategy is trading. This means tracking
    pending positions, updating equity and capital, updating filled positions,
    and updating inventory when fill events are received.

    Parameters
    ----------
    maximum_capacity: Integer.
        An integer representing the maximum number of filled  positions that can
        be held by a portfolio at any given time.
    data_handler: Object inheriting from the abstract data handler class.
        This object supplies the data to update the prices of held positions and
        provide new bar data with which to construct features.
    portfolio_id: String.
        A unique identifier assigned to the portfolio.
    capital: Float.
        The amount of capital (measured in USD) presently held by the portfolio.
    filled_positions (Optional): Dictionary.
        A dictionary of filled position objects mapping symbols to the
        corresponding fill representation.
    """
    def __init__(
            self, maximum_capacity, data_handler, portfolio_id, capital,
            filled_positions=None
    ):
        """Initialize parameters of the portfolio handler object."""
        self.maximum_capacity = maximum_capacity
        self.data_handler = data_handler
        self.portfolio_id = portfolio_id
        self.capital = capital
        self.filled_positions = filled_positions if filled_positions else {}
        self.pending_positions = {}
        self.state = PortfolioState(
            self.capital, self.filled_positions, self.maximum_capacity,
            self.portfolio_id
        )

    def to_database_portfolio(self):
        """Insert the portfolio object into the Odin Securities master database
        so that the capital and position information is persistent across
        trading sessions.
        """
        # Either create an entry or update it depending on whether or not the
        # portfolio already exists in the database.
        does_not_exist = exists.portfolio(self.portfolio_id)
        if does_not_exist:
            inserts.portfolio(self)
        else:
            pid = gets.id_for_portfolio(self.portfolio_id)
            updates.portfolio(self, pid)

        # For each filled position in the portfolio, add it to the database.
        for pos in self.filled_positions.values():
            pos.to_database_position()

        # Commit changes to the database.
        conn.commit()

    @classmethod
    def from_database_portfolio(cls, portfolio_id, data_handler):
        """Create an instance of a portfolio handler object using the relevant
        data from a portfolio database object. This is useful for preserving the
        state of a portfolio between sessions.

        Parameters
        ----------
        portfolio_id: String.
            A portfolio identifier used to select the appropriate records from
            the database corresponding to this portfolio.
        data_handler: Object inheriting from the abstract data handler class.
            This object supplies the data to update the prices of held positions
            and provide new bar data with which to construct features.
        """
        # First get portfolio attributes.
        port = gets.portfolio(portfolio_id)
        max_cap, capital = port["maximum_capacity"], port["capital"]
        pid = port.name
        # Then get corresponding positions.
        positions = gets.positions_for_portfolio_id(pid)
        filled = {
            p: FilledPosition.from_database_position(portfolio_id, p)
            for p in positions
        }

        return cls(
            max_cap, data_handler, portfolio_id, capital, filled
        )

    @property
    def available_capacity(self):
        """Computes the number of equity positions that are currently unfilled.
        This is the difference between the maximum capacity of the portfolio and
        the number of currently filled and pending positions.

        The property raises a value error when the number of positions in the
        portfolio exceeds the maximum capacity.
        """
        filled, pending = self.filled_positions, self.pending_positions
        # Extract the maximum number of positions this portfolio can support.
        max_cap = self.maximum_capacity
        # Compute the combined number of filled and pending positions.
        n_filled = len(filled.values())
        n_pending = len(pending.values())
        n_pos = n_filled + n_pending
        if n_pos > max_cap:
            raise ValueError("Number of positions exceeds portfolio capacity.")

        # Compute the capacity.
        return max_cap - n_pos

    def is_tradeable(self, trade_type):
        """Determine whether or not the provided trade type can be traded by the
        portfolio at the present time.

        Trades that are selling off a position or exiting it completely can
        always be traded because they reduce capacity. Trade types to enter a
        position can only be traded when there is capacity for the position in
        the portfolio.

        Parameters
        ----------
        trade_type: String.
            A string indicating that the trade is either of type 'BUY', 'SELL'
            or 'EXIT'.
        """
        if trade_type in (TradeTypes.sell_trade, TradeTypes.exit_trade):
            # You can always trade if you're exiting the position.
            return True
        elif self.available_capacity > 0:
            # You can always trade if there is still capacity in the portfolio.
            return True
        else:
            # Otherwise you can't trade.
            return False

    def add_filled_position(self, fill_event):
        """When a fill event is received that indicates that a new position has
        been taken up, that new position is recorded in a dictionary of filled
        positions. This function also adjusts the amount of free capital held by
        the portfolio down to reflect that a new position is held.

        This function also removes the corresponding pending position since the
        position has, when this function is called, been filled by the
        brokerage.

        Parameters
        ----------
        fill_event: Fill event object.
            The fill event that will be added to the positions.
        """
        # Extract variables to create the filled position.
        price = fill_event.fill_cost / fill_event.quantity
        symbol = fill_event.symbol
        trade_type = fill_event.trade_type
        direction = fill_event.direction
        quantity = fill_event.quantity
        action = action_dict[(direction, trade_type)]

        # If the position already exists, then raise an error because we
        # shouldn't be adding a new one.
        if symbol in self.filled_positions:
            raise ValueError(
                "Symbol is already in the portfolio and cannot be added."
            )

        # We remove the pending position from the dictionary of such positions
        # and create a new entry in the filled position dictionary.
        pending = self.pending_positions.pop(symbol)
        filled = FilledPosition.from_pending_position(
            pending, fill_event.datetime, price
        )

        # Transact shares (could be either initially or for an existing
        # position).
        filled.transact_shares(action, quantity, price)
        # Set the new position.
        self.filled_positions[symbol] = filled

        # Subtract from capital to reflect the cost of the new investment.
        self.capital -= filled.relative_value + fill_event.commission
        self.state.capital = self.capital

    def modify_filled_position(self, fill_event):
        """Modifies a position when a fill event is received. This includes
        removing the position from the dictionary of filled positions when the
        quantity is reduced to zero.

        Parameters
        ----------
        fill_event: Fill event object.
            The fill event whose position will be modified in the positions.
        """
        # Extract variables.
        symbol = fill_event.symbol
        fill_cost = fill_event.fill_cost
        price = fill_cost / fill_event.quantity
        direction = fill_event.direction
        trade_type = fill_event.trade_type
        quantity = fill_event.quantity
        action = action_dict[(direction, trade_type)]

        # Ensure validity of the symbol by ensuring that it is currently a
        # position within the portfolio.
        if symbol in self.filled_positions:
            filled = self.filled_positions[symbol]
        else:
            raise ValueError(
                "Cannot modify position for {} because the symbol is not in the"
                "portfolio".format(symbol)
            )

        # Transact shares and evaluate whether or not the position has been
        # fully liquidated.
        filled.transact_shares(action, quantity, price)
        if filled.quantity == 0:
            # Delete from the dictionary of filled positions.
            del self.filled_positions[symbol]

            # If we are live trading, then for compliance purposes mark the
            # position as being closed but have it retained.
            if fill_event.is_live:
                # First update the position in the database and then have its
                # contents transferred to the closed positions table.
                filled.to_database_position()
                sid = gets.id_for_symbol(symbol)
                pid = gets.id_for_portfolio(self.portfolio_id)
                inserts.closed_position(sid, pid)
                deletes.position(sid, pid)
                conn.commit()

        # Compute the percentage change of the execution price relative to the
        # average fill price of the asset. Notice that the amount of value
        # retrieved as cash when a position is liquidated depends on whether or
        # not we are long or short the underlying asset.
        #
        # TODO: Make sure this is correct with some rigorous test cases.
        p_chng = (price - filled.avg_price) / filled.avg_price
        if direction == Directions.long_dir:
            value = (1 + p_chng) * filled.avg_price * quantity
        elif direction == Directions.short_dir:
            value = (1 - p_chng) * filled.avg_price * quantity

        # Update the capital holdings of the portfolio.
        if trade_type in (TradeTypes.sell_trade, TradeTypes.exit_trade):
            self.capital += value - fill_event.commission
        elif trade_type == TradeTypes.buy_trade:
            self.capital -= fill_cost + fill_event.commission

        self.state.capital = self.capital

    def add_pending_position(self, order_event):
        """When an order event is initially issued the order is not immediately
        filled. To make note of this, we indicate in a dictionary of pending
        positions that there is a pending position that has not yet been
        completely filled.

        Parameters
        ----------
        order_event: Order event object.
            The order event that will be appended as a pending order to the
            pending positions of the portfolio handler.
        """
        symbol = order_event.symbol
        self.pending_positions[symbol] = PendingPosition(
            symbol, order_event.quantity, order_event.direction,
            order_event.trade_type, order_event.portfolio_id
        )
