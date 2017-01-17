import smtplib
import pickle
from time import sleep
from email.mime.text import MIMEText
from ib.opt import ibConnection, Connection, message
from .abstract_portfolio import AbstractPortfolio
from ..utilities.params import Directions, IB


class InteractiveBrokersPortfolio(AbstractPortfolio):
    """Interactive Brokers Portfolio Class

    The Interactive Brokers portfolio object handles market and fill events in
    live trading or paper trading scenarios when there are transactions with a
    real brokerage.

    The object extends the abstract portfolio object and differs primarily in
    the respect that it saves the current state of the portfolio to file
    whenever there is a change in available price data or a fill event is
    received.

    Parameters
    ----------
    data_handler, position_handler, portfolio_handler: Refer to base class
        documentation.
    account: String.
        Identifier for the Interactive Brokers account with which to trade.
    gmail_and_password (optional): Tuple.
        A tuple (or list-like object) containing the string representation of
        your gmail account address and its password. These are used to send
        automated emails containing the filled trades for your situational
        awareness.
    """
    def __init__(
            self, data_handler, position_handler, portfolio_handler, account,
            gmail_and_password=None
    ):
        """Initialize parameters of the Interactive Brokers Portfolio."""
        super(InteractiveBrokersPortfolio, self).__init__(
            data_handler, position_handler, portfolio_handler
        )
        # Set the account identifier for this portfolio. This should correspond
        # to either the live trading account or the paper trading account.
        self.account = account
        # Now create connections to the Trader Workstation.
        self.conn = ibConnection(
            clientId=IB.portfolio_id.value, port=IB.port.value
        )
        self.conn.register(
            self.__update_portfolio_handler, message.updatePortfolio
        )
        self.conn.register(self.__error_handler, message.error)
        if not self.conn.connect():
            raise ValueError(
                "Odin was unable to connect to the Trader Workstation."
            )

        # If we want to receive email notifications that trades have been
        # filled, then we provide the gmail account and its password.
        self.gmail_and_password = gmail_and_password

    def __update_portfolio_handler(self, msg):
        """Process portfolio update notifications.

        Receive messages from the Trader Workstation related to the status of
        the portfolio.

        Parameters
        ----------
        msg: Interactive Brokers message object.
            A message containing the portfolio-related update information.
        """
        pass

    def __error_handler(self, msg):
        """Process error messages from Interactive Brokers.

        Receive error messages from the Trader Workstation related to the
        portfolio.

        Parameters
        ----------
        msg: Interactive Brokers message object.
            An object containing the parameters of the error to be logged.
        """
        print("Interactive Brokers portfolio error: {}".format(msg))

    def process_post_events(self):
        """Save the portfolio state to the file system.

        Write the portfolio state to file so that it can be accessed again
        during a new session.
        """
        self.portfolio_handler.to_database_portfolio()

    def process_fill_event(self, fill_event):
        """Extension of abstract base class method. The extension implements the
        capability to send email notifications when fill events are received.
        """
        # Call super class method to handle the fill event.
        super(InteractiveBrokersPortfolio, self).process_fill_event(fill_event)

        # Send an email notification containing the details of the fill event.
        #
        # TODO: Would it be better to make server an instance variable so that we
        #       don't have to recreate it every time there's a fill event?
        if self.gmail_and_password is not None:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(*self.gmail_and_pass)
            msg = MIMEText(str(fill_event), "plain", "utf-8")
            msg["From"] = msg["To"] = self.gmail_and_pass[0]
            msg["Subject"] = "Odin Trade Notification"
            server.sendmail(
                self.gmail_and_pass[0], self.gmail_and_pass[0], msg.as_string()
            )
            server.quit()
