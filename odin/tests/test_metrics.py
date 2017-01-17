import pandas as pd
import numpy as np
import unittest
from odin.metrics import *


class MetricsTest(unittest.TestCase):
    def test_compute_sharpe_ratio(self):
        """Check that the computation of the Sharpe ratio is functioning as
        expected. To achieve this, we manually compute the Sharpe ratio and
        compare it against the Sharpe ratio computed by the metrics module.
        """
        vals = [np.nan, 0.01, 0.02, -0.005]
        returns = pd.Series(vals)
        sr_test = compute_sharpe_ratio(returns)
        sr_valid = np.sqrt(252.) * np.mean(vals[1:]) / np.std(vals[1:])
        self.assertEqual(sr_test, sr_valid)

    def test_compute_drawdowns(self):
        """Ensure that the computation of the drawdowns works as expected."""
        vals = [1., 2., 1.5, 1.75, 3.]
        equity = pd.Series(vals)
        dd, dur = compute_drawdowns(equity, False)
        self.assertTrue((dur == [0, 0, 1, 2, 0]).all())
        self.assertTrue((dd == [0, 0, 0.25, 0.125, 0]).all())

if __name__ == "__main__":
    unittest.main()
