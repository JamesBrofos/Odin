# Odin 1.03

A algorithmic trading platform developed in Python. The platform is built to support both research-driven backtesting as well as production deployment for live trading. Odin can be used for either live trading through Interactive Brokers or simulated backtesting. The software currently exists in an alpha state and is actively seeking developers to add features and fix programmatic errors.

This software is provided under the MIT license.


## Features

* **Backtesting** Odin was written with backtesting in mind and it is therefore possible to accurately evaluate strategies on historical data while correctly accounting for transaction costs and commission fees.
* **Event-Driven Architecture** In order to interface more closely with a live-trading system, Odin uses an event-driven architecture rather than a vectorized one. This allows the same strategy implementations in Odin to be utilized in both simulated and live trading.
* **Integration with IB** Odin is built to interface with Interactive Brokers (IB) to execute live trades. As such you can write strategies, backtest them, and deploy them to live trading, all within Odin.
* **PostgreSQL Database** Odin integrates with its own PostgreSQL database to store information on symbols, price data vendors, historical prices, dividends, stock splits, and volumes. This allows data to be served to Odin directly from the filesystem rather than across an internet connection. Odin will also store positions created in live trading for compliance and verification purposes.
* **Performance Metrics** Odin provides a number of performance metrics such as the Sharpe ratio, drawdown, and drawdown duration in order to characterize the performance of backtested portfolios. Odin will also compute measures of equity utilization, such as the average number of positions, to characterize idleness of funds.
* **Fund Simulation** Odin can also simulate funds consisting of multiple portfolios trading their own strategies. For funds, Odin can also perform portfolio equity rebalancing to prevent the equity levels from becoming too lopsided toward a few strategies. Furthermore, Odin will also deduct management fees from the equity levels if so desired.
* **Low-Level Control** Odin allows the user to wield low-level control over the way data is processed. Odin provides control over which ticker symbols are traded, how much equity is transacted in taking up a position, as well as abstract templates that allow users of the software to define their own handlers for use in trading.

Odin is constantly being worked on and improved by its developers. We would be happy to receive pull requests if you have a feature or a bug fix that you want to see included in the main software. Feel free to open a pull request.

Please refer to Odin's issues page for a (partial) list of improvements and planned features that we are aiming on incorporating into Odin.


## Installation

First, download Odin's source code from this repository. Then, to install the library from source for development purposes, execute the command:

```
sudo python3 setup.py install
```

Odin's and Odin Securities' requirements can be installed by navigating into the `odin` directory and then executing the command:

```
pip3 install -r requirements.txt
```

In addition to Odin itself, using the software will also require you to install Odin's accompanying database [Odin Securities](https://github.com/JamesBrofos/Odin-Securities/). Please refer to the referenced Github page for instructions on building and updating the Odin Securities database.


## Citations

Many thanks go to Michael Halls-Moore for originally getting me interested in quantitative finance via his website [Quantstart](https://www.quantstart.com). Certain components of Odin were drawn originally (or heavily inspired by) his tutorial series on [how to build an event-driven backtester](https://www.quantstart.com/articles/Event-Driven-Backtesting-with-Python-Part-I) as well as his backtesting environment [QSTrader](https://github.com/mhallsmoore/qstrader).

Please refer to the `LICENSE` file for information on copyright and rights granted to users of the software.


## Trading Disclaimer

Trading equities on margin carries a high level of risk, and may not be suitable for all investors. Past performance is not indicative of future results. The high degree of leverage can work against you as well as for you. Before deciding to invest in equities you should carefully consider your investment objectives, level of experience, and risk appetite. The possibility exists that you could sustain a loss of some or all of your initial investment and therefore you should not invest money that you cannot afford to lose. You should be aware of all the risks associated with equities trading, and seek advice from an independent financial advisor if you have any doubts.
