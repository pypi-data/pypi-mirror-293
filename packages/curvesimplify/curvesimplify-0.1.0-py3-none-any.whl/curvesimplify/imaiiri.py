"""Graph-based simplification by Imai and Iri."""

import numpy as np
from curvesimilarities.frechet import decision_problem, fd
from numba import njit

__all__ = [
    "min_num",
    "min_err",
]


EPSILON = np.finfo(np.float64).eps


@njit(cache=True)
def min_num(curve, err, err_type="frechet"):
    """Simplification to minimum vertex number with given error."""
    G = np.empty((len(curve), len(curve)), dtype=np.bool_)
    if err_type == "frechet":
        for i in range(G.shape[0] - 1):
            G[i, i + 1] = 1
            for j in range(i + 2, G.shape[1]):
                subcurve = curve[i : j + 1]
                shortcut = np.concatenate((curve[i : i + 1], curve[j : j + 1]))
                G[i, j] = decision_problem(subcurve, shortcut, err)

    # Dynamic programming
    path_count, predecessor = _traverse_graph(curve, G)

    # Backtracking
    ret = np.empty((path_count[-1], curve.shape[1]), dtype=curve.dtype)
    ret_idx = len(ret) - 1
    curve_idx = len(curve) - 1
    while ret_idx >= 0:
        ret[ret_idx] = curve[curve_idx]
        curve_idx = predecessor[curve_idx]
        ret_idx -= 1

    return ret


@njit(cache=True)
def _traverse_graph(curve, G):
    NUM_INF = len(curve) + 1  # vertex count that is large enough
    path_count = np.empty(len(curve), dtype=np.int_)
    predecessor = np.empty(len(curve), dtype=np.int_)
    path_count[0] = 1
    for i in range(1, len(curve)):
        counts = np.full(i, NUM_INF, dtype=np.int_)
        for j in range(i):
            if G[j, i]:
                counts[j] = path_count[j] + 1
        pre_idx = np.argmin(counts)
        predecessor[i] = pre_idx
        path_count[i] = counts[pre_idx]
    return path_count, predecessor


@njit(cache=True)
def min_err(curve, ell, err_type="frechet"):
    """Simplification to minimum error with given number of vertices."""
    G = np.empty((len(curve), len(curve)), dtype=np.float64)
    if err_type == "frechet":
        for i in range(G.shape[0] - 1):
            G[i, i + 1] = 0
            for j in range(i + 2, G.shape[1]):
                subcurve = curve[i : j + 1]
                shortcut = np.concatenate((curve[i : i + 1], curve[j : j + 1]))
                G[i, j] = fd(subcurve, shortcut)

    crit_val = np.unique(np.triu(G[:-2, 1:]))

    start, end = 0, len(crit_val) - 1
    while end - start > 1:
        mid = (start + end) // 2
        path_count, predecessor = _traverse_graph(curve, G <= crit_val[mid])
        if path_count[-1] > ell:
            start = mid
        else:
            end = mid
    if path_count[-1] > ell:  # Run one last time
        path_count, predecessor = _traverse_graph(curve, G <= crit_val[end])
    err = crit_val[end]

    # Backtracking
    ret = np.empty((path_count[-1], curve.shape[1]), dtype=curve.dtype)
    ret_idx = len(ret) - 1
    curve_idx = len(curve) - 1
    while ret_idx >= 0:
        ret[ret_idx] = curve[curve_idx]
        curve_idx = predecessor[curve_idx]
        ret_idx -= 1

    return ret, err
