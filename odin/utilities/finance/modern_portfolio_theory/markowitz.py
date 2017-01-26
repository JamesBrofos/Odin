import numpy as np
import pandas as pd
from cvxopt import matrix
from cvxopt.blas import dot
from cvxopt.solvers import qp, options
options["show_progress"] = False


def solve_markowitz(prices, omega=1.0):
    """This method solves the modern portfolio theory quadratic program to
    deduce the optimal weight configuration. Subject to the constraint that the
    weights be non-negative and that they sum to one, modern portfolio theory
    seeks to minimize risk for a specified level of return. This can be
    equivalently interpreted as a trade-off between variance and risk level,
    with the ultimate criterion to be optimized being the reward-to-risk ratio,
    commonly known as the Sharpe ratio.

    A common criticism of modern portfolio theory is that it is susceptible to
    investing all of the liquidity into a single asset. This problem is present
    in this implementation as well, though it can be mitigated slightly via the
    upper bound parameter omega.

    Parameters
    ----------
    prices: Pandas DataFrame.
        A DataFrame object containing the historical (adjusted) prices for
        specific assets. Assets that do not have the full range of data due to
        becoming recently listed on the exchange are dropped and ignored.
    omega (optional): Float.
        A value between zero and one corresponding to the upper limit on the
        proportion of capital that can be placed into any one asset.
    """
    # Number of assets.
    pct = prices.pct_change().ix[1:].dropna(axis=1)
    n = pct.shape[1]
    # Assert that the upper bound on the allocation of an individual asset is
    # not too low.
    if omega < 1. / n:
        omega = 1.0

    # Compute mean and covariance of the historical percentage change of the
    # stock prices.
    mu = pct.mean()
    mu_mat = matrix(mu)
    S = pct.cov().values
    S_mat = matrix(S)

    # Inequality constraints. These constrain the weights to be non-negative.
    G = matrix(np.vstack((-np.eye(n), np.eye(n))))
    h = matrix(0.0, (2*n, 1))
    h[n:] = omega

    # Equality constraints. These constrain the weights to sum to unity.
    A = matrix(1.0, (1, n))
    b = matrix(1.0)

    # Number of intermittent values of the weight assigned to covariance to try.
    N = 100
    # Vector in which to store the results of the quadratic program. We store
    # not only the weights, but also the corresponding expected return and
    # variance of the portfolio.
    X = np.empty((N, n+2))
    X[:] = np.nan

    for i, m in enumerate(np.logspace(-1, 4, num=N)):
        try:
            res = qp(matrix(m*S_mat), -mu_mat, G, h, A, b)
        except ValueError:
            continue
        else:
            x = np.abs(np.array(res["x"]).ravel())

        if res["status"] == "optimal":
            X[i, :n] = x
            X[i, n] = mu.dot(x)
            X[i, n+1] = np.sqrt(x.dot(S).dot(x))

    # Compute the risk-to-reward ratio for each value of the expected return and
    # determine the maximum.
    X = X[~np.isnan(X).any(axis=1)]
    sharpe = X[:, n+1] / X[:, n]
    opt = X[sharpe.argmax()]
    cols = list(pct.columns)
    cols.extend(["reward", "risk"])
    ret = {c: opt[i] for i, c in enumerate(cols)}

    # Return the weights, the expected reward, and the risk as a Pandas series.
    return ret
