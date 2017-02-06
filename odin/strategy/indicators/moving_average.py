import numpy as np


class MovingAverage(object):
    """Moving Average Class

    Provides support for both simple moving averages and exponential moving
    averages
    """
    def __init__(self, window):
        """Initialize parameters of the moving average object."""
        self.window = window

    def simple_moving_average(self, series):
        """Implementation of a simple moving average."""
        return series.ix[-self.window:].mean()

    def simple_z_score(self, series):
        """Implementation of a simple z-score."""
        recent = series.ix[-self.window:]
        return (series.ix[-1] - recent.mean()) / recent.std()

    def exponential_moving_average(self, series, alpha):
        """Implementation of an exponential moving average."""
        weights = np.array([(1 - alpha) ** i for i in range(self.window)])
        return (series.ix[-self.window:] * weights).sum()
