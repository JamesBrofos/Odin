import numpy as np
import pandas as pd
from cvxopt import matrix
from cvxopt.blas import dot
from cvxopt.solvers import qp, options
options["show_progress"] = False


def solve_black_litterman(prices):
    """This method solves the Black-Litterman asset allocation problem.
    Generally viewed as an improvement over the Markowitz mean-variance
    portfolio allocation methodology, Black-Litterman takes a Bayesian approach
    to incorporating market views into the optimization problem.

    TODO: Figure out how Black-Litterman actually works.
    """
    # Number of assets.
    pct = prices.pct_change().ix[1:].dropna(axis=1)
    n = pct.shape[1]

    # Compute the covariance of the historical percentage changes.
    S = pct.cov().values
