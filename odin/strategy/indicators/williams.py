


class Williams(object):
    """Williams %R Class

    Williams %R, or just %R, is a technical analysis oscillator showing the
    current closing price in relation to the high and low of the past N days
    (for a given N). It was developed by a publisher and promoter of trading
    materials, Larry Williams. Its purpose is to tell whether a stock or
    commodity market is trading near the high or the low, or somewhere in
    between, of its recent trading range.

    The oscillator is on a negative scale, from −100 (lowest) up to 0 (highest),
    obverse of the more common 0 to 100 scale found in many Technical Analysis
    oscillators. A value of −100 means the close today was the lowest low of the
    past N days, and 0 means today's close was the highest high of the past N
    days.

    Source: https://en.wikipedia.org/wiki/Williams_%25R
    """
    def __init__(self, window):
        """Initialize parameters of the moving average object."""
        self.window = window

    def percent_r(self, bars):
        """Implementation of Williams' %R."""
        rec = bars.ix[:, -self.window:, :]
        high, low = rec["adj_price_high"].max(), rec["adj_price_low"].min()
        close = rec.ix["adj_price_close", -1, :]
        return (high - close) / (high - low) * -100.0

